# Network Scanner for Home Assistant

**Version 2.0.3**
**Built by [OnOff Automations](https://onoffautomations.com)**

A network scanning addon for Home Assistant that discovers devices on your local network with a modern web interface accessible via side panel or direct access.

## Features

- **Manual Network Scanning**: Click to scan your network on demand
- **Multi-Subnet Support**: Scan multiple subnets with easy UI to add/remove
- **Configurable Port Scanning**: Change ports to scan directly from the UI
- **Device Information**: IP, hostname, MAC address, vendor, open ports
- **Clickable Port Badges**: Click any port to open that service
  - SSH ports (22) open styled SSH connection helper
  - Non-standard ports show styled modal with HTTP/HTTPS links
  - Standard ports (80, 443) open directly
- **Status Indicators**: Green dot for online devices, red for offline
- **Ping Tool**: Test device connectivity with visual ping results (8 pings at a time)
- **Auto-refresh Toggle**: Enable/disable automatic refresh (on by default, refreshes every 5 seconds)
- **Modern Dark UI**: Accessible via Home Assistant sidebar
- **Device Actions**: Dropdown menu with Ping, HTTP/HTTPS/SSH/RTSP, and copy options
- **Export Options**: Export results as JSON or CSV (works with ingress and direct access)
- **Remote Access**: Works remotely via Home Assistant - always scans local network where HA is installed
- **Persistent Results**: Accumulates devices across multiple scans

## Quick Installation

### Option 1: Add-on Store (Recommended)
1. Navigate to **Supervisor** > **Add-on Store**
2. Click three dots (top right) > **Repositories**
3. Add your repository URL
4. Find "Network Scanner" and click **Install**
5. Click **Start**
6. Click **Network Scanner** in Home Assistant sidebar

### Option 2: Manual Installation
1. Copy this folder to `/addons/network_scanner/` in your HA config directory
2. Restart Home Assistant
3. Go to **Supervisor** > **Add-on Store**
4. Find "Network Scanner" and click **Install**
5. Click **Start**

## Quick Start

1. **Access**: Click **Network Scanner** in Home Assistant sidebar
2. **Configure Ports**: Enter ports to scan in the "Ports to Scan" field (e.g., `22,80,443,8123`)
3. **Add Subnets**: Type subnet and press Enter (e.g., `192.168.2.0/24`)
4. **Scan**: Click "Scan Network" button
5. **View Devices**: See discovered devices with all information
6. **Actions**: Click dropdown on each device to open services or copy info
7. **Export**: Export results as JSON or CSV

## Configuration

Access via **Supervisor** > **Network Scanner** > **Configuration**:

```yaml
scan_interval: 300                    # Not used (manual scan only)
ports_to_scan: "22,80,443,8123"      # Ports to scan on each device
web_port: 8099                        # Port for direct access
enable_mac_vendor: true               # Enable MAC vendor lookup
enable_hostname_lookup: true          # Enable hostname resolution
```

## Access Methods

### Via Home Assistant Sidebar (Ingress)
- Click **Network Scanner** in sidebar
- Works locally and remotely
- Always scans local network where HA is installed

### Direct Access
- `http://homeassistant.local:8099/`
- Replace `homeassistant.local` with your HA IP
- Useful for local network testing

## Support

For detailed configuration, troubleshooting, and API documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

**Issues?** Check the documentation or contact OnOff Automations.

---

**Built by [OnOff Automations](https://onoffautomations.com)**
