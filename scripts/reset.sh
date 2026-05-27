#!/bin/sh
set -e

echo "========================================================"
echo "  Resetting Environment and Database Volumes           "
echo "========================================================"

echo "--> Stopping containers and destroying persistent volumes..."
docker compose down -v

echo "--> Cleaning up runtime files and python cache blocks..."
# For Windows/Linux compatibility, execute cleanups gracefully
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "========================================================"
echo "  Reset complete. Run 'make bootstrap' to rebuild.     "
echo "========================================================"
