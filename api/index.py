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
            'service': 'aiqtoolkit-nvidia-platform',
            'version': '1.1.0',
            'timestamp': int(time.time()),
            'components': [
                {
                    'name': 'Report Generator',
                    'status': 'active',
                    'endpoint': '/api/generate'
                },
                {
                    'name': 'NVIDIA Integration',
                    'status': 'active',
                    'endpoint': '/api/nvidia'
                },
                {
                    'name': 'Reasoning Engine',
                    'status': 'active',
                    'endpoint': '/api/reasoning'
                }
            ],
            'documentation': 'https://github.com/plturrell/finsightdeep'
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
            
            response_data = {
                'message': 'Welcome to AIQToolkit NVIDIA Platform API',
                'available_endpoints': [
                    '/api/health - Check system health',
                    '/api/generate - Generate reports and content',
                    '/api/nvidia - Access NVIDIA AI models',
                    '/api/reasoning - Use advanced reasoning capabilities'
                ],
                'timestamp': int(time.time())
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'message': f'Server error: {str(e)}',
                'service': 'api_index'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()