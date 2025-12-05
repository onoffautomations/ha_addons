#!/usr/bin/with-contenv bashio

bashio::log.info "Starting Network Scanner..."

CONFIG_PATH=/data/options.json

SCAN_INTERVAL=$(bashio::config 'scan_interval')
PORTS=$(bashio::config 'ports_to_scan')
WEB_PORT=$(bashio::config 'web_port')
ENABLE_MAC_VENDOR=$(bashio::config 'enable_mac_vendor')
ENABLE_HOSTNAME=$(bashio::config 'enable_hostname_lookup')

bashio::log.info "Configuration:"
bashio::log.info "  Scan interval: ${SCAN_INTERVAL} seconds"
bashio::log.info "  Ports to scan: ${PORTS}"
bashio::log.info "  Web port: ${WEB_PORT}"

export SCAN_INTERVAL
export PORTS_TO_SCAN=${PORTS}
export WEB_PORT
export ENABLE_MAC_VENDOR
export ENABLE_HOSTNAME_LOOKUP=${ENABLE_HOSTNAME}

cd /app

bashio::log.info "Starting web server..."
bashio::log.info "Access via Home Assistant sidebar or http://homeassistant.local:${WEB_PORT}"

exec python3 -u server.py
