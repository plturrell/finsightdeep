from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('generate-api')

# Default NVIDIA API endpoints
NVIDIA_API_ENDPOINT = "https://api.nvidia.com/v1/chat/completions"
NVIDIA_NIM_ENDPOINT = os.environ.get('NIM_BASE_URL', 'https://api.nvidia.com/nim/v1')

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
            messages = data.get('messages', [{'role': 'user', 'content': 'No input provided'}])
            model = data.get('model', 'llama-3.1-70b-instruct')
            temperature = data.get('temperature', 0.7)
            max_tokens = data.get('max_tokens', 1000)
            format = data.get('format', 'markdown')
            include_sources = data.get('include_sources', False)
            
            # API key and endpoint config
            nvidia_api_key = data.get('nvidia_api_key') or os.environ.get('NVIDIA_API_KEY', '')
            nvidia_endpoint = data.get('nvidia_endpoint') or os.environ.get('NVIDIA_ENDPOINT', NVIDIA_NIM_ENDPOINT)
            use_nim = data.get('use_nim', True)
            
            logger.info(f"Generate request received for model: {model}, format: {format}")
            
            if not nvidia_endpoint:
                # Return error if no endpoint configured
                error_response = {
                    'error': 'NVIDIA endpoint not configured. Please set NVIDIA_ENDPOINT environment variable.',
                    'status': 'error'
                }
                logger.error("Missing NVIDIA endpoint configuration")
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Try to make actual call to NVIDIA endpoint
            try:
                # Prepare the request to NVIDIA
                nvidia_request_data = {
                    'messages': messages,
                    'model': model,
                    'max_tokens': max_tokens,
                    'temperature': temperature
                }
                
                # Log request (without showing the entire message content for privacy)
                logger.info(f"Sending request to NVIDIA: model={model}, temp={temperature}, max_tokens={max_tokens}")
                start_time = time.time()
                
                # Determine which API endpoint to use
                if use_nim:
                    endpoint_url = f"{nvidia_endpoint}/chat/completions"
                    service_name = "NVIDIA NIM"
                else:
                    endpoint_url = NVIDIA_API_ENDPOINT
                    service_name = "NVIDIA API"
                
                logger.info(f"Using {service_name} endpoint: {endpoint_url}")
                
                # Add request headers
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                
                if nvidia_api_key:
                    headers['Authorization'] = f'Bearer {nvidia_api_key}'
                
                # Make request to NVIDIA endpoint
                req = urllib.request.Request(
                    endpoint_url,
                    data=json.dumps(nvidia_request_data).encode('utf-8'),
                    headers=headers
                )
                
                with urllib.request.urlopen(req, timeout=60) as response:
                    nvidia_response = json.loads(response.read().decode())
                    
                    processing_time = time.time() - start_time
                    logger.info(f"NVIDIA response received in {processing_time:.2f}s")
                    
                    # Extract the actual response from NVIDIA
                    if 'choices' in nvidia_response and len(nvidia_response['choices']) > 0:
                        actual_response = nvidia_response['choices'][0]['message']['content']
                        
                        # Format response if needed
                        if format == 'html' and actual_response.strip():
                            # Simple markdown to HTML conversion for demo
                            actual_response = self.markdown_to_html(actual_response)
                    else:
                        actual_response = str(nvidia_response)
                    
                    # Include sources if requested
                    sources = []
                    if include_sources and 'context' in nvidia_response:
                        sources = nvidia_response.get('context', {}).get('documents', [])
                    
                    # Return the real NVIDIA response
                    response_data = {
                        'response': actual_response,
                        'nvidia_endpoint': nvidia_endpoint,
                        'status': 'success',
                        'model': model,
                        'messages': messages,
                        'format': format,
                        'processing_time': round(processing_time, 2),
                        'usage': nvidia_response.get('usage', {}),
                        'sources': sources if include_sources else [],
                        'source': service_name
                    }
                    
                    self.wfile.write(json.dumps(response_data).encode())
                    
            except urllib.error.URLError as e:
                # NVIDIA endpoint not reachable - provide helpful fallback
                error_message = str(e.reason) if hasattr(e, 'reason') else str(e)
                logger.error(f"URLError connecting to NVIDIA: {error_message}")
                
                fallback_response = {
                    'response': f'Unable to reach NVIDIA endpoint at {nvidia_endpoint}.\n\nError: {error_message}\n\nThis could mean:\n1. The endpoint is offline\n2. Network connectivity issues\n3. Authentication required\n4. Endpoint URL is incorrect\n\nPlease verify your NVIDIA endpoint configuration.',
                    'nvidia_endpoint': nvidia_endpoint,
                    'status': 'endpoint_error',
                    'model': model,
                    'messages': messages,
                    'error_details': error_message,
                    'source': 'error_handler'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
                
            except urllib.error.HTTPError as e:
                # HTTP error from NVIDIA endpoint
                status_code = e.code if hasattr(e, 'code') else 500
                error_body = e.read().decode() if hasattr(e, 'read') else str(e)
                logger.error(f"HTTP Error {status_code} from NVIDIA: {error_body}")
                
                fallback_response = {
                    'response': f'NVIDIA API HTTP Error {status_code}: {error_body}\n\nThis usually means:\n- Invalid API key\n- Model not available\n- Rate limit exceeded\n- Authentication required',
                    'nvidia_endpoint': nvidia_endpoint,
                    'status': 'http_error',
                    'model': model,
                    'messages': messages,
                    'error_details': error_body,
                    'error_code': status_code,
                    'source': 'error_handler'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
                
            except Exception as nvidia_error:
                # Other NVIDIA API errors
                logger.error(f"Error calling NVIDIA: {str(nvidia_error)}")
                
                fallback_response = {
                    'response': f'NVIDIA API error: {str(nvidia_error)}\n\nThis appears to be an issue with the NVIDIA service or API format. Please check your endpoint configuration and try again.',
                    'nvidia_endpoint': nvidia_endpoint,
                    'status': 'api_error',
                    'model': model,
                    'messages': messages,
                    'error_details': str(nvidia_error),
                    'source': 'nvidia_error'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'error': f'Server error: {str(e)}',
                'status': 'server_error'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def markdown_to_html(self, markdown_text):
        """Simple markdown to HTML conversion for demo purposes"""
        # Convert headers
        html = markdown_text
        for i in range(6, 0, -1):
            pattern = '\n' + ('#' * i) + ' '
            if i == 1:
                html = html.replace(pattern, '\n<h1>')
                html = html.replace('\n# ', '\n<h1>')
                html = html.replace('\n<h1>', '\n<h1>', 1)  # Avoid double replacement
                html = html.replace('\n', '</h1>\n', 1)
            else:
                html = html.replace(pattern, f'\n<h{i}>')
                html = html.replace(f'\n<h{i}>', f'</h{i-1}>\n<h{i}>', 1)
        
        # Convert code blocks
        html = html.replace('```', '<pre><code>')
        html = html.replace('</code></pre>', '</code></pre>')
        
        # Convert bold and italic
        html = html.replace('**', '<strong>')
        html = html.replace('</strong>', '</strong>')
        html = html.replace('*', '<em>')
        html = html.replace('</em>', '</em>')
        
        # Convert lists
        html = html.replace('\n- ', '\n<li>')
        html = html.replace('</li>', '</li>')
        
        # Wrap in HTML document
        html = f"<div class='markdown-content'>{html}</div>"
        
        return html
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()