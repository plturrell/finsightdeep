from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        test_response = {
            "status": "success",
            "message": "Reasoning API is operational",
            "endpoints": {
                "/api/reasoning": "POST - Generate transparent AI reasoning",
                "/api/generate": "POST - Standard AI generation",
                "/api/nvidia": "POST - NVIDIA service integration"
            },
            "test_query": {
                "url": "/api/reasoning",
                "method": "POST",
                "body": {
                    "query": "What is the best approach to optimize AI model performance?",
                    "model": "o1-preview"
                }
            }
        }
        
        self.wfile.write(json.dumps(test_response, indent=2).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()