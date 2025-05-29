from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('health-check')

# Production NVIDIA endpoints
NVIDIA_API_ENDPOINT = "https://api.nvidia.com/v1/chat/completions"
NVIDIA_NIM_ENDPOINT = os.environ.get('NIM_BASE_URL', 'https://api.nvidia.com/nim/v1')
NVIDIA_NEMO_ENDPOINT = "https://api.nvidia.com/nemo/retriever/v1"
NVIDIA_RIVA_ENDPOINT = "https://api.nvidia.com/riva/v1"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Get NVIDIA endpoint from environment or use default
        nvidia_endpoint = os.environ.get('NVIDIA_ENDPOINT', NVIDIA_NIM_ENDPOINT)
        
        response = {
            'status': 'healthy',
            'service': 'aiqtoolkit-nvidia-proxy',
            'nvidia_endpoint': nvidia_endpoint,
            'version': '1.1.0',
            'timestamp': int(time.time()),
            'services': {
                'nvidia_api': {
                    'endpoint': NVIDIA_API_ENDPOINT,
                    'status': 'unknown'
                },
                'nvidia_nim': {
                    'endpoint': nvidia_endpoint,
                    'status': 'unknown'
                },
                'nvidia_nemo': {
                    'endpoint': NVIDIA_NEMO_ENDPOINT,
                    'status': 'unknown'
                },
                'nvidia_riva': {
                    'endpoint': NVIDIA_RIVA_ENDPOINT,
                    'status': 'unknown'
                }
            }
        }
        
        self.wfile.write(json.dumps(response).encode())
    
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
            
            endpoint = data.get('endpoint', '')
            service = data.get('service', 'unknown')
            api_key = data.get('api_key', os.environ.get('NVIDIA_API_KEY', ''))
            
            if not endpoint:
                response_data = {
                    'status': 'error',
                    'message': 'No endpoint provided',
                    'service': service
                }
                self.wfile.write(json.dumps(response_data).encode())
                return
            
            # Try to connect to the endpoint
            headers = {
                'Accept': 'application/json'
            }
            
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            try:
                logger.info(f"Testing connection to {service} at {endpoint}")
                start_time = time.time()
                
                req = urllib.request.Request(
                    endpoint,
                    headers=headers
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    status_code = response.getcode()
                    processing_time = time.time() - start_time
                    
                    # Try to read response
                    try:
                        response_body = response.read().decode()
                        try:
                            response_json = json.loads(response_body)
                        except:
                            response_json = {}
                    except:
                        response_json = {}
                    
                    logger.info(f"Connection to {service} successful in {processing_time:.2f}s")
                    
                    response_data = {
                        'status': 'success',
                        'message': f'Successfully connected to {service}',
                        'service': service,
                        'status_code': status_code,
                        'version': response_json.get('version', 'unknown'),
                        'latency_ms': int(processing_time * 1000),
                        'data': response_json
                    }
            
            except urllib.error.HTTPError as e:
                error_body = e.read().decode() if hasattr(e, 'read') else str(e)
                logger.error(f"HTTP Error {e.code} connecting to {service}: {error_body}")
                response_data = {
                    'status': 'error',
                    'message': f'HTTP Error: {e.code}',
                    'service': service,
                    'status_code': e.code,
                    'error_details': error_body
                }
            
            except urllib.error.URLError as e:
                logger.error(f"Connection Error to {service}: {str(e.reason)}")
                response_data = {
                    'status': 'error',
                    'message': f'Connection Error: {str(e.reason)}',
                    'service': service,
                    'error_details': str(e)
                }
            
            except Exception as e:
                logger.error(f"Unknown error connecting to {service}: {str(e)}")
                response_data = {
                    'status': 'error',
                    'message': f'Error: {str(e)}',
                    'service': service,
                    'error_details': str(e)
                }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            error_response = {
                'status': 'error',
                'message': f'Server error: {str(e)}',
                'service': 'health_check'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()