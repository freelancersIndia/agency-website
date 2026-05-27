#!/bin/sh
set -e

echo "========================================================"
echo "  Bootstrapping WhatsApp Agent Template Platform       "
echo "========================================================"

# Check for .env.example
if [ ! -f ".env.example" ]; then
    echo "Error: .env.example not found in root directory!"
    exit 1
fi

# Copy environment file
if [ ! -f ".env.local" ]; then
    echo "--> Copying .env.example to .env.local..."
    cp .env.example .env.local
else
    echo "--> .env.local already exists, skipping copying step."
fi

# Verify Docker
if command -v docker >/dev/null 2>&1; then
    echo "--> Docker found. Building containers..."
    docker compose build
else
    echo "--> [Warning] docker binary was not found. Please install Docker before booting."
fi

echo "========================================================"
echo "  Bootstrap Completed successfully!                     "
echo "  Execute 'make run' or 'sh ./scripts/dev.sh' to start. "
echo "========================================================"
