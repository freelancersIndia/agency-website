#!/bin/sh
set -e

echo "========================================================"
echo "  Starting Development Services in Foreground           "
echo "========================================================"

if [ ! -f ".env.local" ]; then
    echo "--> .env.local not found. Initiating bootstrap..."
    sh ./scripts/bootstrap.sh
fi

docker compose up
