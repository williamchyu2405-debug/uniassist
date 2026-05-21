#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Run ./setup.sh first"
  exit 1
fi

source venv/bin/activate

if ! grep -q "sk-ant" .env 2>/dev/null; then
  echo ""
  echo "  ⚠️   Please add your Anthropic API key to .env before starting."
  echo "  Open: $(pwd)/.env"
  echo ""
  exit 1
fi

echo ""
echo "  Starting UniAssist…"
echo "  Open in your browser: http://localhost:8000"
echo ""
python3 main.py
