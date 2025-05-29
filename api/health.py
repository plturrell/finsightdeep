from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'service': 'aiqtoolkit-nvidia-proxy',
            'nvidia_endpoint': os.environ.get('NVIDIA_ENDPOINT', 'https://jupyter0-s1ondnjfx.brevlab.com'),
            'version': '1.0.0',
            'timestamp': int(time.time())
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
            api_key = data.get('api_key', '')
            
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
                req = urllib.request.Request(
                    endpoint,
                    headers=headers
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    status_code = response.getcode()
                    
                    # Try to read response
                    try:
                        response_body = response.read().decode()
                        try:
                            response_json = json.loads(response_body)
                        except:
                            response_json = {}
                    except:
                        response_json = {}
                    
                    response_data = {
                        'status': 'success',
                        'message': f'Successfully connected to {service}',
                        'service': service,
                        'status_code': status_code,
                        'version': response_json.get('version', 'unknown'),
                        'data': response_json
                    }
            
            except urllib.error.HTTPError as e:
                response_data = {
                    'status': 'error',
                    'message': f'HTTP Error: {e.code}',
                    'service': service,
                    'status_code': e.code,
                    'error_details': str(e)
                }
            
            except urllib.error.URLError as e:
                response_data = {
                    'status': 'error',
                    'message': f'Connection Error: {str(e.reason)}',
                    'service': service,
                    'error_details': str(e)
                }
            
            except Exception as e:
                response_data = {
                    'status': 'error',
                    'message': f'Error: {str(e)}',
                    'service': service,
                    'error_details': str(e)
                }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
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