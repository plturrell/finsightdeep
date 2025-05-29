from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

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
            service_type = data.get('service_type', 'chat')  # chat, embeddings, completion
            model = data.get('model', 'llama-3.1-70b-instruct')
            nvidia_api_key = data.get('nvidia_api_key') or os.environ.get('NVIDIA_API_KEY')
            custom_endpoint = data.get('nvidia_endpoint') or os.environ.get('NVIDIA_ENDPOINT')
            
            # Determine which NVIDIA service to use
            if service_type == 'nim':
                response_data = self.call_nvidia_nim(prompt, model, custom_endpoint, nvidia_api_key)
            elif service_type == 'nemo':
                response_data = self.call_nvidia_nemo(prompt, model, nvidia_api_key)
            elif service_type == 'triton':
                response_data = self.call_nvidia_triton(prompt, model, custom_endpoint)
            else:
                # Default to NVIDIA API
                response_data = self.call_nvidia_api(prompt, model, nvidia_api_key)
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'error': f'Server error: {str(e)}',
                'status': 'server_error',
                'service': 'nvidia_proxy'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def call_nvidia_api(self, prompt, model, api_key):
        """Call official NVIDIA API"""
        try:
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
                'https://api.nvidia.com/v1/chat/completions',
                data=json.dumps(nvidia_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nvidia_response = json.loads(response.read().decode())
                
                if 'choices' in nvidia_response and len(nvidia_response['choices']) > 0:
                    content = nvidia_response['choices'][0]['message']['content']
                    return {
                        'response': content,
                        'status': 'success',
                        'model': model,
                        'service': 'nvidia_api',
                        'usage': nvidia_response.get('usage', {}),
                        'source': 'https://api.nvidia.com'
                    }
                else:
                    return {
                        'response': f'Unexpected response format from NVIDIA API: {nvidia_response}',
                        'status': 'format_error',
                        'service': 'nvidia_api'
                    }
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else str(e)
            return {
                'response': f'NVIDIA API HTTP Error {e.code}: {error_body}\n\nThis usually means:\n- Invalid API key\n- Model not available\n- Rate limit exceeded\n- Authentication required',
                'status': 'http_error',
                'service': 'nvidia_api',
                'error_code': e.code
            }
        except Exception as e:
            return {
                'response': f'NVIDIA API Error: {str(e)}',
                'status': 'api_error',
                'service': 'nvidia_api'
            }
    
    def call_nvidia_nim(self, prompt, model, custom_endpoint, api_key):
        """Call NVIDIA NIM (NVIDIA Inference Microservices)"""
        if not custom_endpoint:
            return {
                'response': 'NVIDIA NIM endpoint not configured. Please provide nvidia_endpoint parameter.',
                'status': 'config_error',
                'service': 'nvidia_nim'
            }
        
        try:
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
            
            req = urllib.request.Request(
                f"{custom_endpoint}/v1/chat/completions",
                data=json.dumps(nim_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nim_response = json.loads(response.read().decode())
                
                if 'choices' in nim_response and len(nim_response['choices']) > 0:
                    content = nim_response['choices'][0]['message']['content']
                    return {
                        'response': content,
                        'status': 'success',
                        'model': model,
                        'service': 'nvidia_nim',
                        'endpoint': custom_endpoint,
                        'usage': nim_response.get('usage', {})
                    }
                else:
                    return {
                        'response': f'Unexpected response from NIM: {nim_response}',
                        'status': 'format_error',
                        'service': 'nvidia_nim'
                    }
                    
        except Exception as e:
            return {
                'response': f'NVIDIA NIM Error: {str(e)}\n\nEndpoint: {custom_endpoint}\n\nPlease verify your NIM endpoint is running and accessible.',
                'status': 'nim_error',
                'service': 'nvidia_nim',
                'endpoint': custom_endpoint
            }
    
    def call_nvidia_nemo(self, prompt, model, api_key):
        """Call NVIDIA NeMo Service"""
        try:
            nemo_request = {
                'prompt': prompt,
                'model': model,
                'max_length': 1000,
                'temperature': 0.7
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            req = urllib.request.Request(
                'https://api.nvidia.com/v1/nemo/generate',
                data=json.dumps(nemo_request).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                nemo_response = json.loads(response.read().decode())
                
                return {
                    'response': nemo_response.get('text', str(nemo_response)),
                    'status': 'success',
                    'model': model,
                    'service': 'nvidia_nemo'
                }
                
        except Exception as e:
            return {
                'response': f'NVIDIA NeMo Error: {str(e)}',
                'status': 'nemo_error',
                'service': 'nvidia_nemo'
            }
    
    def call_nvidia_triton(self, prompt, model, custom_endpoint):
        """Call NVIDIA Triton Inference Server"""
        if not custom_endpoint:
            return {
                'response': 'NVIDIA Triton endpoint not configured.',
                'status': 'config_error',
                'service': 'nvidia_triton'
            }
        
        try:
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
                    'endpoint': custom_endpoint
                }
                
        except Exception as e:
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