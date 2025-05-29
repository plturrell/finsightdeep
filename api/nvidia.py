from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('nvidia-api')

# Production NVIDIA API endpoints
NVIDIA_API_ENDPOINT = "https://api.nvidia.com/v1/chat/completions"
NVIDIA_NEMO_ENDPOINT = "https://api.nvidia.com/nemo/retriever/v1"
NVIDIA_RIVA_ENDPOINT = "https://api.nvidia.com/riva/v1"
NVIDIA_ACE_ENDPOINT = "https://api.nvidia.com/ace/v1"
NVIDIA_TOKKIO_ENDPOINT = "https://api.nvidia.com/tokkio/v1"

# Default API key from environment variable
DEFAULT_API_KEY = os.environ.get('NVIDIA_API_KEY', '')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode())
            else:
                data = {}
            
            # Extract parameters
            prompt = data.get('prompt', '')
            service_type = data.get('service_type', 'chat')  # chat, embeddings, completion, retriever, riva, ace, tokkio
            model = data.get('model', 'llama-3.1-70b-instruct')
            nvidia_api_key = data.get('nvidia_api_key') or os.environ.get('NVIDIA_API_KEY') or DEFAULT_API_KEY
            custom_endpoint = data.get('nvidia_endpoint') or os.environ.get('NVIDIA_ENDPOINT')
            
            # Log request (omitting sensitive information)
            logger.info(f"Request received for service: {service_type}, model: {model}")
            
            # Determine which NVIDIA service to use
            if service_type == 'nim':
                response_data = self.call_nvidia_nim(prompt, model, custom_endpoint, nvidia_api_key)
            elif service_type == 'nemo':
                response_data = self.call_nvidia_nemo(prompt, model, nvidia_api_key)
            elif service_type == 'riva':
                response_data = self.call_nvidia_riva(prompt, model, nvidia_api_key)
            elif service_type == 'ace':
                response_data = self.call_nvidia_ace(prompt, model, nvidia_api_key)
            elif service_type == 'tokkio':
                response_data = self.call_nvidia_tokkio(prompt, model, nvidia_api_key)
            elif service_type == 'triton':
                response_data = self.call_nvidia_triton(prompt, model, custom_endpoint)
            else:
                # Default to NVIDIA Chat API
                response_data = self.call_nvidia_api(prompt, model, nvidia_api_key)
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            error_response = {
                'error': f'Server error: {str(e)}',
                'status': 'server_error',
                'service': 'nvidia_proxy'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def call_nvidia_api(self, prompt, model, api_key):
        """Call official NVIDIA API for chat completions"""
        try:
            logger.info(f"Calling NVIDIA API with model: {model}")
            start_time = time.time()
            
            nvidia_request = {
                'messages': [{'role': 'user', 'content': prompt}],
                'model': model,
                'max_tokens': 1000,
                'temperature': 0.7,
                'top_p': 1,
                'stream': False
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                NVIDIA_API_ENDPOINT,
                data=json.dumps(nvidia_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nvidia_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"NVIDIA API response received in {processing_time:.2f}s")
                
                if 'choices' in nvidia_response and len(nvidia_response['choices']) > 0:
                    content = nvidia_response['choices'][0]['message']['content']
                    return {
                        'response': content,
                        'status': 'success',
                        'model': model,
                        'service': 'nvidia_api',
                        'usage': nvidia_response.get('usage', {}),
                        'source': NVIDIA_API_ENDPOINT,
                        'processing_time': processing_time
                    }
                else:
                    logger.warning(f"Unexpected response format: {nvidia_response}")
                    return {
                        'response': f'Unexpected response format from NVIDIA API: {nvidia_response}',
                        'status': 'format_error',
                        'service': 'nvidia_api'
                    }
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else str(e)
            logger.error(f"HTTP Error {e.code}: {error_body}")
            return {
                'response': f'NVIDIA API HTTP Error {e.code}: {error_body}\n\nThis usually means:\n- Invalid API key\n- Model not available\n- Rate limit exceeded\n- Authentication required',
                'status': 'http_error',
                'service': 'nvidia_api',
                'error_code': e.code
            }
        except Exception as e:
            logger.error(f"Error calling NVIDIA API: {str(e)}")
            return {
                'response': f'NVIDIA API Error: {str(e)}',
                'status': 'api_error',
                'service': 'nvidia_api'
            }
    
    def call_nvidia_nim(self, prompt, model, custom_endpoint, api_key):
        """Call NVIDIA NIM (NVIDIA Inference Microservices)"""
        if not custom_endpoint:
            # Use production NIM endpoint if custom endpoint not provided
            custom_endpoint = os.environ.get('NIM_BASE_URL', 'https://api.nvidia.com/nim/v1')
        
        try:
            logger.info(f"Calling NVIDIA NIM with model: {model}")
            start_time = time.time()
            
            nim_request = {
                'messages': [{'role': 'user', 'content': prompt}],
                'model': model,
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            endpoint_url = f"{custom_endpoint}/chat/completions"
            logger.info(f"Using NIM endpoint: {endpoint_url}")
            
            req = urllib.request.Request(
                endpoint_url,
                data=json.dumps(nim_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nim_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"NIM response received in {processing_time:.2f}s")
                
                if 'choices' in nim_response and len(nim_response['choices']) > 0:
                    content = nim_response['choices'][0]['message']['content']
                    return {
                        'response': content,
                        'status': 'success',
                        'model': model,
                        'service': 'nvidia_nim',
                        'endpoint': custom_endpoint,
                        'usage': nim_response.get('usage', {}),
                        'processing_time': processing_time
                    }
                else:
                    logger.warning(f"Unexpected NIM response format: {nim_response}")
                    return {
                        'response': f'Unexpected response from NIM: {nim_response}',
                        'status': 'format_error',
                        'service': 'nvidia_nim'
                    }
                    
        except Exception as e:
            logger.error(f"Error calling NVIDIA NIM: {str(e)}")
            return {
                'response': f'NVIDIA NIM Error: {str(e)}\n\nEndpoint: {custom_endpoint}\n\nPlease verify your NIM endpoint is running and accessible.',
                'status': 'nim_error',
                'service': 'nvidia_nim',
                'endpoint': custom_endpoint
            }
    
    def call_nvidia_nemo(self, prompt, model, api_key):
        """Call NVIDIA NeMo Retriever Service"""
        try:
            logger.info(f"Calling NVIDIA NeMo with model: {model}")
            start_time = time.time()
            
            nemo_request = {
                'query': prompt,
                'model': model or 'nvidia/nemo-retriever-embedding-v1',
                'top_k': 5
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                NVIDIA_NEMO_ENDPOINT + '/retrieve',
                data=json.dumps(nemo_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nemo_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"NeMo response received in {processing_time:.2f}s")
                
                results = nemo_response.get('results', [])
                formatted_response = "\n\n".join([f"Source {i+1}: {result.get('text', 'No text')}" for i, result in enumerate(results)])
                
                return {
                    'response': formatted_response or "No relevant results found",
                    'status': 'success',
                    'model': model,
                    'service': 'nvidia_nemo',
                    'results': results,
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"Error calling NVIDIA NeMo: {str(e)}")
            return {
                'response': f'NVIDIA NeMo Error: {str(e)}',
                'status': 'nemo_error',
                'service': 'nvidia_nemo'
            }
    
    def call_nvidia_riva(self, prompt, model, api_key):
        """Call NVIDIA Riva Speech Service"""
        try:
            logger.info(f"Calling NVIDIA Riva with model: {model}")
            start_time = time.time()
            
            riva_request = {
                'text': prompt,
                'language_code': 'en-US',
                'voice_name': model or 'financial_advisor_professional',
                'sample_rate_hz': 22050
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                NVIDIA_RIVA_ENDPOINT + '/tts',
                data=json.dumps(riva_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                riva_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"Riva response received in {processing_time:.2f}s")
                
                # Note: In a real implementation, audio data would be returned as base64
                # Here we'll simulate the response
                return {
                    'response': f"Text-to-speech conversion successful for: '{prompt[:50]}...'",
                    'status': 'success',
                    'model': model,
                    'service': 'nvidia_riva',
                    'audio_format': 'wav',
                    'sample_rate': 22050,
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"Error calling NVIDIA Riva: {str(e)}")
            return {
                'response': f'NVIDIA Riva Error: {str(e)}',
                'status': 'riva_error',
                'service': 'nvidia_riva'
            }
    
    def call_nvidia_ace(self, prompt, model, api_key):
        """Call NVIDIA ACE Service for digital human avatar"""
        try:
            logger.info(f"Calling NVIDIA ACE with model: {model}")
            start_time = time.time()
            
            ace_request = {
                'text': prompt,
                'avatar_model': model or 'audio2face-2d-photorealistic',
                'resolution': [1280, 720],
                'fps': 30
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                NVIDIA_ACE_ENDPOINT + '/generate',
                data=json.dumps(ace_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                ace_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"ACE response received in {processing_time:.2f}s")
                
                # Note: In a real implementation, video data would be returned
                # Here we'll simulate the response
                return {
                    'response': f"Digital human animation generated for: '{prompt[:50]}...'",
                    'status': 'success',
                    'model': model,
                    'service': 'nvidia_ace',
                    'resolution': [1280, 720],
                    'fps': 30,
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"Error calling NVIDIA ACE: {str(e)}")
            return {
                'response': f'NVIDIA ACE Error: {str(e)}',
                'status': 'ace_error',
                'service': 'nvidia_ace'
            }
    
    def call_nvidia_tokkio(self, prompt, model, api_key):
        """Call NVIDIA Tokkio Service for workflow execution"""
        try:
            logger.info(f"Calling NVIDIA Tokkio with workflow: {model}")
            start_time = time.time()
            
            tokkio_request = {
                'input': prompt,
                'workflow_id': model or 'financial_advisor_v1',
                'max_steps': 10
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                NVIDIA_TOKKIO_ENDPOINT + '/execute',
                data=json.dumps(tokkio_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                tokkio_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"Tokkio response received in {processing_time:.2f}s")
                
                output = tokkio_response.get('output', 'No output returned')
                steps = tokkio_response.get('steps', [])
                
                return {
                    'response': output,
                    'status': 'success',
                    'workflow': model,
                    'service': 'nvidia_tokkio',
                    'steps': steps,
                    'step_count': len(steps),
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"Error calling NVIDIA Tokkio: {str(e)}")
            return {
                'response': f'NVIDIA Tokkio Error: {str(e)}',
                'status': 'tokkio_error',
                'service': 'nvidia_tokkio'
            }
    
    def call_nvidia_triton(self, prompt, model, custom_endpoint):
        """Call NVIDIA Triton Inference Server"""
        if not custom_endpoint:
            logger.error("Triton endpoint not configured")
            return {
                'response': 'NVIDIA Triton endpoint not configured.',
                'status': 'config_error',
                'service': 'nvidia_triton'
            }
        
        try:
            logger.info(f"Calling NVIDIA Triton with model: {model}")
            start_time = time.time()
            
            triton_request = {
                'inputs': [
                    {
                        'name': 'text_input',
                        'shape': [1],
                        'datatype': 'BYTES',
                        'data': [prompt]
                    }
                ]
            }
            
            req = urllib.request.Request(
                f"{custom_endpoint}/v2/models/{model}/infer",
                data=json.dumps(triton_request).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                triton_response = json.loads(response.read().decode())
                
                processing_time = time.time() - start_time
                logger.info(f"Triton response received in {processing_time:.2f}s")
                
                # Extract output from Triton response
                outputs = triton_response.get('outputs', [])
                if outputs and len(outputs) > 0:
                    output_data = outputs[0].get('data', ['No output'])
                    response_text = output_data[0] if output_data else 'No response'
                else:
                    response_text = str(triton_response)
                
                return {
                    'response': response_text,
                    'status': 'success',
                    'model': model,
                    'service': 'nvidia_triton',
                    'endpoint': custom_endpoint,
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"Error calling NVIDIA Triton: {str(e)}")
            return {
                'response': f'NVIDIA Triton Error: {str(e)}\n\nEndpoint: {custom_endpoint}',
                'status': 'triton_error',
                'service': 'nvidia_triton'
            }
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()