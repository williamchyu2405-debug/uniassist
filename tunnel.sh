#!/bin/bash
# UniAssist — Cloudflare Tunnel
# Run this whenever you want classmates to access UniAssist over the internet.
# The public URL is printed below — share it with your crew.
# Keep this Terminal window open while they're using it.

cd "$(dirname "$0")"

# Make sure UniAssist server is running
if ! curl -s http://localhost:8000/api/access-check > /dev/null 2>&1; then
  echo ""
  echo "  ⚠️   UniAssist doesn't seem to be running."
  echo "  Start it first with ./start.sh, then re-run this."
  echo ""
  exit 1
fi

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║   UniAssist — Public Tunnel                  ║"
echo "  ║   Waiting for Cloudflare URL…                ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""
echo "  Access code required: check your .env for ACCESS_CODE"
echo "  Share the https://... URL that appears below with your classmates."
echo "  Close this window to shut down the tunnel."
echo ""

./cloudflared tunnel --url http://localhost:8000
