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
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode())
            else:
                data = {}
            
            prompt = data.get('prompt', 'No prompt provided')
            model = data.get('model', 'nvidia-model')
            nvidia_endpoint = data.get('nvidia_endpoint') or os.environ.get('NVIDIA_ENDPOINT')
            
            if not nvidia_endpoint:
                # Return error if no endpoint configured
                error_response = {
                    'error': 'NVIDIA endpoint not configured. Please set NVIDIA_ENDPOINT environment variable.',
                    'status': 'error'
                }
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Try to make actual call to NVIDIA endpoint
            try:
                # Prepare the request to NVIDIA
                nvidia_request_data = {
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'model': model,
                    'max_tokens': 1000,
                    'temperature': 0.7
                }
                
                # Make request to NVIDIA endpoint
                req = urllib.request.Request(
                    f"{nvidia_endpoint}/v1/chat/completions",
                    data=json.dumps(nvidia_request_data).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    nvidia_response = json.loads(response.read().decode())
                    
                    # Extract the actual response from NVIDIA
                    if 'choices' in nvidia_response and len(nvidia_response['choices']) > 0:
                        actual_response = nvidia_response['choices'][0]['message']['content']
                    else:
                        actual_response = str(nvidia_response)
                    
                    # Return the real NVIDIA response
                    response_data = {
                        'response': actual_response,
                        'nvidia_endpoint': nvidia_endpoint,
                        'status': 'success',
                        'model': model,
                        'prompt': prompt,
                        'raw_nvidia_response': nvidia_response,
                        'source': 'nvidia_api'
                    }
                    
                    self.wfile.write(json.dumps(response_data).encode())
                    
            except urllib.error.URLError as e:
                # NVIDIA endpoint not reachable - provide helpful fallback
                fallback_response = {
                    'response': f'Unable to reach NVIDIA endpoint at {nvidia_endpoint}.\n\nError: {str(e)}\n\nThis could mean:\n1. The endpoint is offline\n2. Network connectivity issues\n3. Authentication required\n4. Endpoint URL is incorrect\n\nPlease verify your NVIDIA endpoint configuration.',
                    'nvidia_endpoint': nvidia_endpoint,
                    'status': 'endpoint_error',
                    'model': model,
                    'prompt': prompt,
                    'error_details': str(e),
                    'source': 'error_handler'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
                
            except Exception as nvidia_error:
                # Other NVIDIA API errors
                fallback_response = {
                    'response': f'NVIDIA API error: {str(nvidia_error)}\n\nPrompt was: "{prompt}"\n\nThis appears to be an issue with the NVIDIA service or API format. Please check your endpoint configuration and try again.',
                    'nvidia_endpoint': nvidia_endpoint,
                    'status': 'api_error',
                    'model': model,
                    'prompt': prompt,
                    'error_details': str(nvidia_error),
                    'source': 'nvidia_error'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'error': f'Server error: {str(e)}',
                'status': 'server_error'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()