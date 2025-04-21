#!/usr/bin/env python
import subprocess
import os
import sys
import threading

def run_backend():
    print("Starting backend server...")
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_dir)
    subprocess.Popen([sys.executable, 'run.py'])

def run_frontend():
    print("Starting frontend application...")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    os.chdir(frontend_dir)
    subprocess.Popen([sys.executable, 'run.py'])

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Crop Disease Detection System')
    parser.add_argument('--component', choices=['backend', 'frontend', 'all'], 
                        default='all', help='Component to run (default: all)')
    
    args = parser.parse_args()
    
    if args.component == 'backend':
        run_backend()
    elif args.component == 'frontend':
        run_frontend()
    elif args.component == 'all':
        backend_thread = threading.Thread(target=run_backend)
        frontend_thread = threading.Thread(target=run_frontend)
        
        backend_thread.start()
        threading.Timer(5.0, frontend_thread.start).start()
        
        try:
            while True:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            print("\nShutting down...")