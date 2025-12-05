#!/usr/bin/env python3
import nmap
import socket
import subprocess
import re
import netifaces
import os
import json
import time
from datetime import datetime
from mac_vendor_lookup import MacLookup
from threading import Thread, Lock

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.mac_lookup = None
        self.mac_vendor_enabled = False

        # Try to initialize MAC vendor lookup, but don't crash if it fails
        try:
            import os
            os.makedirs('/root/.cache', exist_ok=True)
            self.mac_lookup = MacLookup()
            self.mac_lookup.update_vendors()
            self.mac_vendor_enabled = True
            print("MAC vendor lookup initialized successfully")
        except Exception as e:
            print(f"Warning: MAC vendor lookup disabled due to error: {e}")
            self.mac_vendor_enabled = False

        self.scan_results = []
        self.scan_lock = Lock()
        self.is_scanning = False

    def get_default_gateway_subnet(self):
        """Get the default gateway and subnet"""
        try:
            gws = netifaces.gateways()
            default_gateway = gws['default'][netifaces.AF_INET][0]
            default_interface = gws['default'][netifaces.AF_INET][1]

            addrs = netifaces.ifaddresses(default_interface)
            ip_info = addrs[netifaces.AF_INET][0]
            ip_addr = ip_info['addr']
            netmask = ip_info['netmask']

            subnet = self.calculate_subnet(ip_addr, netmask)
            return subnet
        except Exception as e:
            print(f"Error getting subnet: {e}")
            return "192.168.1.0/24"

    def calculate_subnet(self, ip, netmask):
        """Calculate subnet from IP and netmask"""
        ip_parts = list(map(int, ip.split('.')))
        mask_parts = list(map(int, netmask.split('.')))

        network = [str(ip_parts[i] & mask_parts[i]) for i in range(4)]

        cidr = sum([bin(int(x)).count('1') for x in mask_parts])

        return '.'.join(network) + '/' + str(cidr)

    def get_hostname(self, ip):
        """Get hostname from IP address"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return ""

    def get_mac_vendor(self, mac):
        """Get MAC vendor information"""
        if not self.mac_vendor_enabled or not self.mac_lookup:
            return "Unknown"
        try:
            vendor = self.mac_lookup.lookup(mac)
            return vendor
        except Exception as e:
            return "Unknown"

    def scan_ports(self, ip, ports):
        """Scan specific ports on an IP"""
        open_ports = []
        try:
            self.nm.scan(ip, ports, arguments='-T4')

            if ip in self.nm.all_hosts():
                for proto in self.nm[ip].all_protocols():
                    lport = self.nm[ip][proto].keys()
                    for port in lport:
                        port_state = self.nm[ip][proto][port]['state']
                        port_name = self.nm[ip][proto][port].get('name', '')
                        if port_state == 'open':
                            open_ports.append({
                                'port': port,
                                'state': port_state,
                                'service': port_name
                            })
        except Exception as e:
            print(f"Error scanning ports for {ip}: {e}")

        return open_ports

    def get_arp_table(self):
        """Get ARP table to find MAC addresses"""
        arp_table = {}
        try:
            if os.name == 'posix':
                output = subprocess.check_output(['arp', '-a'], universal_newlines=True)
                for line in output.split('\n'):
                    match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-fA-F:]{17})', line)
                    if match:
                        ip = match.group(1)
                        mac = match.group(2).upper()
                        arp_table[ip] = mac
            else:
                output = subprocess.check_output(['arp', '-a'], universal_newlines=True)
                for line in output.split('\n'):
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})', line)
                    if match:
                        ip = match.group(1)
                        mac = match.group(2).replace('-', ':').upper()
                        arp_table[ip] = mac
        except Exception as e:
            print(f"Error getting ARP table: {e}")

        return arp_table

    def ping_sweep(self, subnet):
        """Perform ping sweep to find live hosts"""
        live_hosts = []
        try:
            print(f"Performing host discovery on {subnet}...")
            self.nm.scan(hosts=subnet, arguments='-sn -T4')

            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    live_hosts.append(host)

        except Exception as e:
            print(f"Error during ping sweep: {e}")

        return live_hosts

    def scan_network(self, subnet="auto", ports="22,80,443,8123", enable_mac_vendor=True, enable_hostname=True):
        """Main network scanning function"""
        try:
            with self.scan_lock:
                self.is_scanning = True
                # Keep existing results - don't clear
                # Remove duplicates based on IP address
                existing_ips = {device['ip'] for device in self.scan_results}
                # self.scan_results = []
            if subnet == "auto":
                subnet = self.get_default_gateway_subnet()

            print(f"Starting network scan on {subnet}")
            print(f"Ports to scan: {ports}")

            live_hosts = self.ping_sweep(subnet)
            print(f"Found {len(live_hosts)} live hosts")

            arp_table = self.get_arp_table()

            for idx, ip in enumerate(live_hosts, 1):
                print(f"Scanning {idx}/{len(live_hosts)}: {ip}")

                device_info = {
                    'ip': ip,
                    'hostname': '',
                    'mac': '',
                    'vendor': '',
                    'ports': [],
                    'last_seen': datetime.now().isoformat(),
                    'status': 'online'
                }

                if enable_hostname:
                    device_info['hostname'] = self.get_hostname(ip)

                if ip in arp_table:
                    device_info['mac'] = arp_table[ip]
                    if enable_mac_vendor and device_info['mac']:
                        device_info['vendor'] = self.get_mac_vendor(device_info['mac'])

                if ports:
                    device_info['ports'] = self.scan_ports(ip, ports)

                # Update or add device
                with self.scan_lock:
                    # Check if device already exists (by IP)
                    existing_idx = next((i for i, d in enumerate(self.scan_results) if d['ip'] == ip), None)
                    if existing_idx is not None:
                        # Update existing device
                        self.scan_results[existing_idx] = device_info
                    else:
                        # Add new device
                        self.scan_results.append(device_info)

            print(f"Scan complete. Total devices: {len(self.scan_results)}")

        except Exception as e:
            print(f"Error during network scan: {e}")
            import traceback
            traceback.print_exc()
        finally:
            with self.scan_lock:
                self.is_scanning = False

        return self.scan_results

    def get_results(self):
        """Get current scan results"""
        with self.scan_lock:
            return {
                'devices': self.scan_results.copy(),
                'total_devices': len(self.scan_results),
                'is_scanning': self.is_scanning,
                'last_update': datetime.now().isoformat()
            }

    def is_scan_running(self):
        """Check if a scan is currently running"""
        with self.scan_lock:
            return self.is_scanning

if __name__ == "__main__":
    scanner = NetworkScanner()
    subnet = os.getenv('SUBNET', 'auto')
    ports = os.getenv('PORTS_TO_SCAN', '22,80,443,8123')

    results = scanner.scan_network(subnet=subnet, ports=ports)
    print(json.dumps(results, indent=2))
