# Network Scanner - Complete Documentation

**Version 2.0.3**
**Built by [OnOff Automations](https://onoffautomations.com)**

---

## Table of Contents

1. [Configuration Options](#configuration-options)
2. [Features](#features)
3. [Port Scanning](#port-scanning)
4. [API Endpoints](#api-endpoints)
5. [Network Requirements](#network-requirements)
6. [Troubleshooting](#troubleshooting)
7. [Technical Details](#technical-details)

---

## Configuration Options

Configure via **Supervisor** > **Network Scanner** > **Configuration**:

| Option | Type | Range | Default | Description |
|--------|------|-------|---------|-------------|
| `scan_interval` | int | 60-3600 | 300 | Not used (manual scan only) |
| `ports_to_scan` | string | - | "22,80,443,8123" | Comma-separated ports to scan |
| `web_port` | int | 1024-65535 | 8099 | Port for direct access |
| `enable_mac_vendor` | bool | - | true | Enable MAC vendor lookup |
| `enable_hostname_lookup` | bool | - | true | Enable hostname resolution |

### Example Configuration

```yaml
scan_interval: 300
ports_to_scan: "22,80,443,8123,3389,445"
web_port: 8099
enable_mac_vendor: true
enable_hostname_lookup: true
```

### Changing Configuration

1. Go to **Supervisor** > **Network Scanner** > **Configuration**
2. Modify values
3. Click **Save**
4. Click **Restart** for changes to take effect

---

## Features

### Manual Network Scanning
- Click "Scan Network" to scan on demand
- No automatic scanning - you control when to scan
- Scan progress shown in real-time

### Multi-Subnet Support
- Type subnet in input field (e.g., `192.168.2.0/24`)
- Press **Enter** to add subnet
- Click **X** to remove subnet
- Scan multiple subnets simultaneously

### Device Information
Each discovered device shows:
- **IP Address**: Device IP on network
- **Hostname**: Resolved hostname (if available)
- **MAC Address**: Hardware address
- **Vendor**: Device manufacturer (via MAC lookup)
- **Open Ports**: List of detected open ports

### Device Actions
Dropdown menu for each device:
- **Open in Browser**: HTTP (80), HTTPS (443)
- **Connect**: SSH (22), RTSP (554)
- **Copy**: IP Address, MAC Address, Hostname, Vendor

### Export Options
- **Export JSON**: Download all results as JSON file
- **Export CSV**: Download all results as CSV file
- Useful for documentation or further analysis

### Remote Access
- Access via Home Assistant sidebar works remotely
- When accessing remotely, scans local network where HA is installed
- Works with Nabu Casa or other remote access methods

### Persistent Results
- Device list accumulates across scans
- Devices persist until page refresh
- Useful for tracking intermittent devices

---

## Port Scanning

### Common Ports

| Port | Service | Description |
|------|---------|-------------|
| 22 | SSH | Secure Shell (remote terminal) |
| 80 | HTTP | Web server |
| 443 | HTTPS | Secure web server |
| 8123 | HA | Home Assistant |
| 3389 | RDP | Remote Desktop Protocol |
| 445 | SMB | Windows file sharing |
| 21 | FTP | File Transfer Protocol |
| 23 | Telnet | Insecure remote terminal |
| 554 | RTSP | Real Time Streaming Protocol (cameras) |

### Customizing Ports

Edit `ports_to_scan` in configuration:
```yaml
ports_to_scan: "22,80,443,8123,554,3389"
```

**Note**: More ports = slower scan time per device.

---

## API Endpoints

The addon provides a REST API for advanced integration:

### `GET /api/status`
Get current scanner status.

**Response:**
```json
{
  "is_scanning": false,
  "config": {
    "scan_interval": 300,
    "ports": "22,80,443,8123",
    "enable_mac_vendor": true,
    "enable_hostname": true
  }
}
```

### `POST /api/scan`
Trigger a new network scan.

**Request Body:**
```json
{
  "subnets": ["auto"],
  "ports": "22,80,443,8123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Scan started"
}
```

### `GET /api/results`
Get current scan results.

**Response:**
```json
{
  "devices": [
    {
      "ip": "192.168.1.100",
      "hostname": "device-name",
      "mac": "AA:BB:CC:DD:EE:FF",
      "vendor": "Device Manufacturer",
      "ports": [80, 443],
      "last_seen": "2025-12-04T10:30:00"
    }
  ],
  "total": 1
}
```

### `GET /api/export/json`
Export results as JSON file (triggers download).

### `GET /api/export/csv`
Export results as CSV file (triggers download).

### `GET /api/ingress_check`
Health check endpoint for Home Assistant ingress.

**Response:**
```json
{
  "status": "ok",
  "service": "network_scanner",
  "version": "2.0.3"
}
```

---

## Network Requirements

### Host Network Mode
- The addon uses `host_network: true`
- This allows direct access to your local network
- Required for ARP scanning and port detection

### Network Access
- Home Assistant host must have network access to devices
- Devices must be on same network or routable subnet
- Some devices may have firewalls blocking scans

### Permissions
- Addon runs with network scanning privileges
- Uses `nmap` and `arp-scan` tools
- Requires root access inside container

---

## Troubleshooting

### No Devices Found

**Causes:**
- Subnet configured incorrectly
- Devices powered off
- Network firewall blocking

**Solutions:**
1. Use "auto" for automatic subnet detection
2. Verify devices are powered on and connected
3. Check Home Assistant network configuration
4. Try direct access: `http://homeassistant.local:8099`

### Slow Scanning

**Causes:**
- Too many ports configured
- Large subnet range
- Slow network

**Solutions:**
1. Reduce ports to scan: `ports_to_scan: "22,80,443"`
2. Scan specific subnets instead of large ranges
3. Scan fewer devices at once

### Missing MAC Addresses

**Causes:**
- Device hasn't communicated recently
- ARP table not populated
- Device not on local subnet

**Solutions:**
1. Ping device first: `ping 192.168.1.100`
2. Scan again after device communicates
3. Check device is on same network

### MAC Vendor Lookup Fails

**Causes:**
- No internet connection
- Vendor database not accessible
- Unknown MAC address

**Solutions:**
1. Disable if not needed: `enable_mac_vendor: false`
2. Check internet connectivity
3. Vendor may show as "Unknown" for some devices

### 503 Error on Side Panel

**Causes:**
- Addon not started
- Port conflict
- Ingress proxy issue

**Solutions:**
1. Check addon status: **Supervisor** > **Network Scanner**
2. Check logs for startup errors
3. Restart addon
4. Restart Home Assistant if needed

### 404 Error When Scanning

**Causes:**
- Old JavaScript cached in browser
- API path issue

**Solutions:**
1. **Clear browser cache**: `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)
2. Try incognito/private window
3. Check browser console (F12) for errors
4. Verify version 2.0.3 in addon logs

### Direct Access Works, Ingress Doesn't

**Causes:**
- Browser cache has old JavaScript
- Ingress proxy issue

**Solutions:**
1. **Hard refresh**: `Ctrl + Shift + R`
2. Clear all browser cache
3. Restart Home Assistant
4. Check addon logs show ingress requests

### Copy to Clipboard Not Working

**Causes:**
- Browser permission denied
- Insecure context (HTTP)

**Solutions:**
1. Allow clipboard permission in browser
2. Use HTTPS if possible
3. Manually select and copy text

---

## Technical Details

### Architecture

**Components:**
- **Flask**: Web framework
- **Waitress**: Production WSGI server
- **ProxyFix**: Middleware for ingress support
- **nmap**: Network scanner
- **arp-scan**: MAC address detection
- **mac-vendor-lookup**: Vendor identification

**Files:**
- `config.yaml`: Addon configuration
- `Dockerfile`: Container build instructions
- `build.yaml`: Multi-architecture support
- `run.sh`: Startup script
- `server.py`: Flask web server
- `scanner.py`: Network scanning logic
- `requirements.txt`: Python dependencies
- `web/index.html`: Web interface

### Ingress Support

The addon supports Home Assistant ingress for sidebar access:

**How it works:**
1. User clicks sidebar icon
2. HA proxies request to addon via ingress path
3. JavaScript detects ingress path automatically
4. All API calls use correct path
5. Works seamlessly both local and remote

**Ingress paths:**
- Direct: `http://homeassistant.local:8099/`
- Ingress: `https://your-ha.com/api/hassio_ingress/TOKEN/`

**Path detection:**
```javascript
function getBasePath() {
    const path = window.location.pathname;
    return path.endsWith('/') ? path : path + '/';
}
```

This automatically works for both access methods!

### Multi-Architecture Support

Supports the following architectures:
- `armhf` - ARM 32-bit (older Raspberry Pi)
- `armv7` - ARM 32-bit v7 (Raspberry Pi 2/3)
- `aarch64` - ARM 64-bit (Raspberry Pi 4, newer)
- `amd64` - Intel/AMD 64-bit
- `i386` - Intel/AMD 32-bit

### Logging

Full request/response logging for debugging:

**Check logs:**
```
Supervisor > Network Scanner > Logs
```

**What to look for:**
- `Starting Waitress server on 0.0.0.0:8099`
- `→ GET /` (incoming requests)
- `← 200 /` (successful responses)
- `API call: /api/hassio_ingress/.../api/scan` (in browser console)

---

## Version History

### v2.0.3 (Current)
- ✅ Fixed API 404 errors when using ingress
- ✅ Smart base path detection for API calls
- ✅ Works with both direct and ingress access
- ✅ All features functional remotely

### v2.0.2
- ✅ Deep 503 fixes with catch-all routes
- ✅ Health check endpoints
- ✅ Full request logging

### v2.0.1
- ✅ Switched to Waitress + ProxyFix
- ✅ Configurable web port
- ✅ OnOff Automations link

### v2.0.0
- ✅ Simplified addon approach
- ✅ Removed NGINX proxy
- ✅ Side panel support

---

## Privacy & Security

### Data Collection
- All scanning performed locally on your network
- No telemetry or usage data sent externally
- MAC vendor lookups use public API (if enabled)

### Network Security
- Web interface only accessible within your network (or via HA ingress)
- No external ports exposed
- Uses Home Assistant's built-in security

### Recommendations
1. Use strong Home Assistant passwords
2. Enable 2FA if accessing remotely
3. Keep Home Assistant and addons updated
4. Use HTTPS for remote access

---

## Support

**Documentation**: This file
**Website**: [onoffautomations.com](https://onoffautomations.com)
**Version**: 2.0.3

**Built by [OnOff Automations](https://onoffautomations.com)**
