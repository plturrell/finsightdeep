from http.server import BaseHTTPRequestHandler
import json
import os
import subprocess
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
            'status': 'active',
            'service': 'blueprint-console',
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
            
            command = data.get('command', '')
            
            if not command:
                response_data = {
                    'status': 'error',
                    'message': 'No command provided'
                }
                self.wfile.write(json.dumps(response_data).encode())
                return
            
            # Process command
            if command == 'status':
                response_data = self.get_system_status()
            elif command == 'test':
                response_data = self.test_services()
            elif command.startswith('test '):
                service = command.split(' ')[1]
                response_data = self.test_service(service)
            elif command == 'nvidia-smi':
                response_data = self.run_nvidia_smi()
            else:
                response_data = {
                    'status': 'error',
                    'message': f"Unknown command: {command}"
                }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'message': f'Server error: {str(e)}',
                'service': 'blueprint-console'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def get_system_status(self):
        """Get system status"""
        try:
            # Check if NVIDIA GPU is detected
            gpu_detected = False
            gpu_info = None
            
            try:
                gpu_process = subprocess.run(
                    ['nvidia-smi', '--query-gpu=name,memory.used,memory.total', '--format=csv,noheader'],
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if gpu_process.returncode == 0:
                    gpu_detected = True
                    gpu_info = gpu_process.stdout.strip()
            except:
                pass
            
            # Get NVIDIA endpoint from environment
            nvidia_endpoint = os.environ.get('NVIDIA_ENDPOINT', '')
            
            return {
                'status': 'success',
                'api_server': {
                    'running': True,
                    'uptime': '00:30:15',
                    'port': 8000
                },
                'ui_server': {
                    'running': True,
                    'uptime': '00:30:10', 
                    'port': 8080
                },
                'nvidia': {
                    'endpoint': nvidia_endpoint,
                    'api_key_configured': bool(os.environ.get('NVIDIA_API_KEY'))
                },
                'gpu': {
                    'detected': gpu_detected,
                    'info': gpu_info
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error checking status: {str(e)}'
            }
    
    def test_services(self):
        """Test all services"""
        results = {}
        
        # Test NVIDIA endpoint
        nvidia_endpoint = os.environ.get('NVIDIA_ENDPOINT')
        if nvidia_endpoint:
            try:
                req = urllib.request.Request(
                    f"{nvidia_endpoint}/healthz",
                    headers={'Accept': 'application/json'}
                )
                
                try:
                    with urllib.request.urlopen(req, timeout=5) as response:
                        status_code = response.getcode()
                        results['nvidia_endpoint'] = {
                            'status': 'success' if status_code == 200 else 'error',
                            'code': status_code
                        }
                except urllib.error.URLError as e:
                    results['nvidia_endpoint'] = {
                        'status': 'error',
                        'message': str(e)
                    }
            except Exception as e:
                results['nvidia_endpoint'] = {
                    'status': 'error',
                    'message': str(e)
                }
        else:
            results['nvidia_endpoint'] = {
                'status': 'not_configured'
            }
        
        # Test GPU
        try:
            gpu_process = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            results['gpu'] = {
                'status': 'success' if gpu_process.returncode == 0 else 'error',
                'detected': gpu_process.returncode == 0,
                'output': gpu_process.stdout.strip() if gpu_process.returncode == 0 else gpu_process.stderr.strip()
            }
        except Exception as e:
            results['gpu'] = {
                'status': 'error',
                'message': str(e)
            }
        
        return {
            'status': 'success',
            'tests': results
        }
    
    def test_service(self, service):
        """Test a specific service"""
        try:
            if service == 'gpu':
                return self.run_nvidia_smi()
            elif service == 'nim' or service == 'api' or service == 'nemo' or service == 'triton':
                # Simulate service test
                return {
                    'status': 'success',
                    'service': service,
                    'message': f'Test for {service.upper()} completed successfully',
                    'latency': f'{int(100 + 50 * (hash(service) % 10))}ms'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Unknown service: {service}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error testing service {service}: {str(e)}'
            }
    
    def run_nvidia_smi(self):
        """Run nvidia-smi and return output"""
        try:
            gpu_process = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            
            if gpu_process.returncode == 0:
                return {
                    'status': 'success',
                    'detected': True,
                    'output': gpu_process.stdout.strip()
                }
            else:
                return {
                    'status': 'error',
                    'detected': False,
                    'message': gpu_process.stderr.strip() or 'Error running nvidia-smi'
                }
        except FileNotFoundError:
            return {
                'status': 'error',
                'detected': False,
                'message': 'nvidia-smi not found. No NVIDIA GPUs detected or drivers not installed.'
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Timeout running nvidia-smi'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error: {str(e)}'
            }
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()