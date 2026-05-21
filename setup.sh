#!/bin/bash
set -e

echo ""
echo "  UniAssist Setup"
echo "  ──────────────────────────────────────"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "  ❌  Python 3 not found."
  echo "  Please install it from https://www.python.org/downloads/"
  exit 1
fi

echo "  ✓  Python found: $(python3 --version)"

# Create venv
if [ ! -d "venv" ]; then
  echo "  Creating virtual environment…"
  python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "  Installing dependencies…"
pip install -q -r requirements.txt

# Create .env if missing
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo ""
  echo "  ⚠️   Almost done! Open the file below and add your Anthropic API key:"
  echo "       $(pwd)/.env"
  echo ""
  echo "  Get a free key at: https://console.anthropic.com"
fi

echo ""
echo "  ✅  Setup complete!"
echo "  Run  ./start.sh  to launch UniAssist"
echo ""
