"""
This module includes embedding service from local embedding model or from llm_commons

The following classes are available:

    * :class `PALModelEmbeddings`
    * :class `HANAVectorEmbeddings`
"""

# pylint: disable=redefined-builtin
# pylint: disable=unnecessary-dunder-call
# pylint: disable=unused-argument

from typing import List
import uuid
import sys
import os

import pandas as pd

# Add the parent directory to sys.path to be able to import constants
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from hana_ai.api.env_constants import SAP_AI_CORE_EMBEDDING_MODEL, DEFAULT_GPU_MEMORY_FRACTION
except ImportError:
    # Fallback defaults if not in API context
    SAP_AI_CORE_EMBEDDING_MODEL = "sap-ai-core-embeddings"
    DEFAULT_GPU_MEMORY_FRACTION = 0.8

try:
    from gen_ai_hub.proxy.langchain import init_embedding_model as gen_ai_hub_embedding_model
except:
    pass
from langchain.embeddings.base import Embeddings
from hana_ml.dataframe import ConnectionContext, create_dataframe_from_pandas
from hana_ml.text.pal_embeddings import PALEmbeddings
from hana_ml.algorithms.pal.pal_base import try_drop

class PALModelEmbeddings(Embeddings):
    """
    PAL embedding model.

    Parameters
    ----------
    connection_context : ConnectionContext
        Connection context.
    model_version : str, optional
        Model version. Default to None.
    batch_size : int, optional
        Batch size. Default to None.
    thread_number : int, optional
        Thread number. Default to None.
    is_query : bool, optional
        Use different embedding model for query purpose. Default to None.
    """
    model_version: str
    connection_context: ConnectionContext
    batch_size: int
    thread_number: int
    is_query: bool

    def __init__(self, connection_context, model_version=None, batch_size=None, thread_number=None, is_query=None):
        """
        Init PAL embedding model.
        """
        self.model_version = model_version
        self.connection_context = connection_context
        self.batch_size = batch_size
        self.thread_number = thread_number
        self.is_query = is_query

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        pe = PALEmbeddings(self.model_version)
        temporary_table = "#PAL_EMBEDDINGS_" + str(uuid.uuid4()).replace("-", "_")
        df = create_dataframe_from_pandas(self.connection_context, pandas_df=pd.DataFrame({"ID": range(len(input)), "TEXT": input}), table_name=temporary_table, disable_progressbar=True, table_type="COLUMN")
        result = pe.fit_transform(data=df, key="ID", target="TEXT", thread_number=self.thread_number, batch_size=self.batch_size, is_query=self.is_query)
        self.model_version = pe.stat_.collect().iat[1, 1]
        result = list(map(lambda x: list(x[0]), result[result.columns[-2]].collect().to_numpy()))
        try_drop(self.connection_context, temporary_table)
        try_drop(self.connection_context, pe._fit_output_table_names)
        return result

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.__call__(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.

        Parameters
        ----------
        text : str
            Text.

        Returns
        -------
        List[float]
            Embedding.
        """
        return self.__call__(text)[0]

    def get_text_embedding_batch(self, texts: List[str], show_progress=False, **kwargs):
        """
        Get text embedding batch.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.embed_documents(texts)

class HANAVectorEmbeddings(Embeddings):
    """
    PAL embedding model.

    Parameters
    ----------
    connection_context : ConnectionContext
        Connection context.
    model_version : str, optional
        Model version.  Default to 'SAP_NEB.20240715'
    """
    model_version: str
    connection_context: ConnectionContext

    def __init__(self, connection_context, model_version='SAP_NEB.20240715'):
        """
        Init PAL embedding model.
        """
        self.model_version = model_version
        self.connection_context = connection_context

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return self.connection_context.embed_query(input, model_version=self.model_version)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.__call__(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.

        Parameters
        ----------
        text : str
            Text.

        Returns
        -------
        List[float]
            Embedding.
        """
        return self.__call__(text)[0]

    def get_text_embedding_batch(self, texts: List[str], show_progress=False, **kwargs):
        """
        Get text embedding batch.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.embed_documents(texts)

class GenAIHubEmbeddings(Embeddings):
    """
    A class representing the embedding service for SAP GenAI Hub.

    Parameters
    ----------
    deployment_id: str
        Deployment ID for SAP AI Core model. Defaults to SAP_AI_CORE_EMBEDDING_MODEL.
    """
    model: Embeddings
    def __init__(self, deployment_id=None, **kwargs):
        # Use default if not specified
        if deployment_id is None:
            deployment_id = SAP_AI_CORE_EMBEDDING_MODEL
        """
        Init embedding service from SAP GenAI Hub.
        """
        # Ensure we only use SAP AI Core models
        if not deployment_id.startswith('sap-ai-core'):
            import logging
            logging.warning(f"Non-SAP model requested: {deployment_id}. Defaulting to 'sap-ai-core-embeddings'")
            deployment_id = 'sap-ai-core-embeddings'
            
        # Add NVIDIA GPU optimization if available
        gpu_config = {}
        try:
            from hana_ai.api.config import settings
            if getattr(settings, 'ENABLE_GPU_ACCELERATION', False):
                gpu_config = {
                    "use_gpu": True,
                    "gpu_memory_fraction": getattr(settings, 'CUDA_MEMORY_FRACTION', DEFAULT_GPU_MEMORY_FRACTION),
                }
        except ImportError:
            # If settings not available, use default GPU settings
            gpu_config = {
                "use_gpu": True,
                "gpu_memory_fraction": DEFAULT_GPU_MEMORY_FRACTION,
            }
            
        kwargs.update(gpu_config)
        self.model = gen_ai_hub_embedding_model(deployment_id, **kwargs)

    def __call__(self, input):
        result = []
        if isinstance(input, list):
            result = self.model.embed_documents(input)
        else:
            result.append(self.model.embed_query(input))
        return result

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.model.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.

        Parameters
        ----------
        text : str
            Text.

        Returns
        -------
        List[float]
            Embedding.
        """
        return self.model.embed_query(text)

    def get_text_embedding_batch(self, texts: List[str], show_progress=False, **kwargs):
        """
        Get text embedding batch.

        Parameters
        ----------
        texts : List[str]
            List of texts.

        Returns
        -------
        List[List[float]]
            List of embeddings.
        """
        return self.embed_documents(texts)
