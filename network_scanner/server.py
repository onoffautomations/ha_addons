#!/usr/bin/env python3
"""Network Scanner - Flask server for Home Assistant addon"""
from flask import Flask, send_from_directory, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix
from waitress import serve
import os
import json
import threading
from datetime import datetime
from scanner import NetworkScanner

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Add ProxyFix middleware for Home Assistant ingress support
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_prefix=1
)

# Configuration
SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL', '300'))
PORTS_TO_SCAN = os.getenv('PORTS_TO_SCAN', '22,80,443,8123')
WEB_PORT = int(os.getenv('WEB_PORT', '8099'))
ENABLE_MAC_VENDOR = os.getenv('ENABLE_MAC_VENDOR', 'true').lower() == 'true'
ENABLE_HOSTNAME = os.getenv('ENABLE_HOSTNAME_LOOKUP', 'true').lower() == 'true'

# Initialize scanner
scanner = None

def get_scanner():
    global scanner
    if scanner is None:
        print("Initializing network scanner...", flush=True)
        scanner = NetworkScanner()
        print("Scanner initialized", flush=True)
    return scanner


@app.route('/icon.png')
def serve_icon():
    """Serve addon icon"""
    return send_from_directory('.', 'icon.png')


@app.route('/')
@app.route('/<path:path>')
def catch_all(path=''):
    """Handle all routes - serves index.html for ingress compatibility"""
    if path and not path.startswith('api/'):
        # Try to serve static file
        try:
            return send_from_directory('web', path)
        except:
            pass
    # Default to index.html
    return send_from_directory('web', 'index.html')


@app.route('/ingress_check')
@app.route('/api/ingress_check')
def ingress_check():
    """Health check endpoint for ingress"""
    return jsonify({
        'status': 'ok',
        'service': 'network_scanner',
        'version': '2.0.3'
    }), 200


@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Trigger a new scan"""
    s = get_scanner()

    if s.is_scan_running():
        return jsonify({'status': 'error', 'message': 'Scan already in progress'}), 400

    data = request.get_json() or {}
    subnets = data.get('subnets', ['auto'])
    ports = data.get('ports', PORTS_TO_SCAN)

    if isinstance(subnets, str):
        subnets = [subnets]

    def scan_multiple_subnets():
        try:
            for subnet in subnets:
                if subnet and subnet.strip():
                    print(f"Scanning subnet: {subnet}", flush=True)
                    s.scan_network(subnet, ports, ENABLE_MAC_VENDOR, ENABLE_HOSTNAME)
            print("Scan complete", flush=True)
        except Exception as e:
            print(f"Scan error: {e}", flush=True)
            import traceback
            traceback.print_exc()

    thread = threading.Thread(target=scan_multiple_subnets)
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'success', 'message': 'Scan started'})


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get scan results"""
    s = get_scanner()
    results = s.get_results()
    return jsonify(results)


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get scanner status"""
    s = get_scanner()
    return jsonify({
        'is_scanning': s.is_scan_running(),
        'config': {
            'scan_interval': SCAN_INTERVAL,
            'ports': PORTS_TO_SCAN,
            'enable_mac_vendor': ENABLE_MAC_VENDOR,
            'enable_hostname': ENABLE_HOSTNAME
        }
    })


@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export scan results as JSON"""
    s = get_scanner()
    results = s.get_results()
    return jsonify(results)


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export scan results as CSV"""
    s = get_scanner()
    results = s.get_results()

    # Build CSV content
    csv_lines = ['IP Address,Hostname,MAC Address,Vendor,Open Ports,Last Seen']

    for device in results.get('devices', []):
        ip = device.get('ip', '')
        hostname = device.get('hostname', '')
        mac = device.get('mac', '')
        vendor = device.get('vendor', '')
        ports = ','.join(map(str, device.get('ports', [])))
        last_seen = device.get('last_seen', '')

        # Escape commas in fields
        hostname = f'"{hostname}"' if ',' in hostname else hostname
        vendor = f'"{vendor}"' if ',' in vendor else vendor

        csv_lines.append(f'{ip},{hostname},{mac},{vendor},{ports},{last_seen}')

    csv_content = '\n'.join(csv_lines)

    return jsonify({'csv': csv_content})


@app.before_request
def log_request():
    """Log all requests for debugging"""
    print(f"→ {request.method} {request.path} | Headers: {dict(request.headers)}", flush=True)


@app.after_request
def log_response(response):
    """Log response status"""
    print(f"← {response.status_code} {request.path}", flush=True)
    return response


if __name__ == '__main__':
    print("=" * 60, flush=True)
    print("Network Scanner v2.0.3", flush=True)
    print("Built by OnOff Automations", flush=True)
    print("=" * 60, flush=True)
    print(f"Configuration:", flush=True)
    print(f"  Web Port: {WEB_PORT}", flush=True)
    print(f"  Ports to Scan: {PORTS_TO_SCAN}", flush=True)
    print(f"  MAC Vendor: {ENABLE_MAC_VENDOR}", flush=True)
    print(f"  Hostname Lookup: {ENABLE_HOSTNAME}", flush=True)
    print("=" * 60, flush=True)
    print(f"Starting Waitress server on 0.0.0.0:{WEB_PORT}", flush=True)
    print("Access via:", flush=True)
    print("  - Home Assistant sidebar (ingress)", flush=True)
    print(f"  - http://homeassistant.local:{WEB_PORT} (direct)", flush=True)
    print("=" * 60, flush=True)
    print("Server starting with full request logging enabled...", flush=True)
    print("Ingress health check: /ingress_check", flush=True)
    print("=" * 60, flush=True)

    try:
        # Use Waitress for production-grade WSGI server (handles ingress properly)
        serve(app, host='0.0.0.0', port=WEB_PORT, threads=6, connection_limit=100)
    except Exception as e:
        print(f"FATAL: Server failed to start: {e}", flush=True)
        import traceback
        traceback.print_exc()
        import time
        time.sleep(60)  # Keep container alive to see error
