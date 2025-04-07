Changelog
=========

**Version 1.0.250403**

``New Functions``
    - Added `list_models` tool to list all trained models in the model storage.
    - Added `accuracy_measure` tool to measure the accuracy of a model on a test dataset for time series forecasting.

``Enhancements``
    - Improved the `intermittent_forecast` tool to use CrostonTSB instead.
    - Added parameter `return_direct` to all tools and toolkit.
    - Improved the `fetch_data` tool to return a pandas DataFrame instead of a list of dictionaries. By default, the tool parameter `return_direct` is set to `True`, which means the tool will return a pandas DataFrame.
