#!/usr/bin/env python3
"""
HTTPS server for serving firmware artifacts from the build directory.
Runs on port 8443 and serves metadata.json and build artifacts.
"""

import http.server
import ssl
import os
import sys
import subprocess
from pathlib import Path


class MetadataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metadata.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('metadata.json', 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()


def generate_cert(cert_file, key_file):
    """Generate self-signed certificate if it doesn't exist."""
    if Path(cert_file).exists() and Path(key_file).exists():
        return
    
    print(f"Generating self-signed certificate...")
    cmd = [
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', key_file, '-out', cert_file,
        '-days', '365', '-nodes',
        '-subj', '/CN=10.9.1.196'
    ]
    subprocess.run(cmd, check=True)
    print(f"Certificate generated: {cert_file}")


def main():
    build_dir = Path(__file__).parent.parent / 'build'
    
    if not build_dir.exists():
        print(f"Error: Build directory not found at {build_dir}")
        sys.exit(1)
    
    os.chdir(build_dir)
    
    cert_file = 'server.crt'
    key_file = 'server.key'
    generate_cert(cert_file, key_file)
    
    server = http.server.HTTPServer(('0.0.0.0', 8443), MetadataHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    
    print(f"HTTPS server running on https://0.0.0.0:8443")
    print(f"Serving from: {build_dir}")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)


if __name__ == '__main__':
    main()
