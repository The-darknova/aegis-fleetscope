#!/bin/bash
set -e

# Scaffolding script for Agent packaging (DEB and RPM)
# Requires fpm to be installed: gem install fpm

VERSION=${1:-"1.0.0"}
ITERATION=${2:-"1"}
ARCH=${3:-"amd64"}

echo "Building packages for Aegis Agent v${VERSION}-${ITERATION} (${ARCH})..."

# Define package structure paths
PKG_DIR=$(mktemp -d)
mkdir -p "${PKG_DIR}/opt/aegis-fleetscope/agent/bin"
mkdir -p "${PKG_DIR}/etc/aegis-fleetscope"
mkdir -p "${PKG_DIR}/usr/lib/systemd/system"

# Assuming binaries are built locally in the 'bin' folder
AGENT_BIN="bin/aegis-agent-${ARCH}"

if [ ! -f "${AGENT_BIN}" ]; then
  echo "Error: Agent binary ${AGENT_BIN} not found. Run go build first."
  exit 1
fi

# Copy assets to package layout
cp "${AGENT_BIN}" "${PKG_DIR}/opt/aegis-fleetscope/agent/bin/aegis-agent"
cp packaging/aegis-agent.yaml.example "${PKG_DIR}/etc/aegis-fleetscope/aegis-agent.yaml"
cp packaging/systemd/aegis-agent.service "${PKG_DIR}/usr/lib/systemd/system/"

echo "Generating RPM package..."
fpm -s dir -t rpm \
  --name "aegis-agent" \
  --version "${VERSION}" \
  --iteration "${ITERATION}" \
  --architecture "${ARCH}" \
  --description "Aegis FleetScope Go Agent" \
  --maintainer "admin@aegis-fleetscope.local" \
  -C "${PKG_DIR}" .

echo "Generating DEB package..."
fpm -s dir -t deb \
  --name "aegis-agent" \
  --version "${VERSION}" \
  --iteration "${ITERATION}" \
  --architecture "${ARCH}" \
  --description "Aegis FleetScope Go Agent" \
  --maintainer "admin@aegis-fleetscope.local" \
  -C "${PKG_DIR}" .

rm -rf "${PKG_DIR}"
echo "Packaging complete."
