#!/bin/bash
# MailTrace — Quick Start (SQLite mode)
# No PostgreSQL required for local development

set -e

cd "$(dirname "$0")"

# Clear stale Python caches to prevent stale code from loading
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

export DATABASE_URL="sqlite:///./mailtrace.db"
export DEMO_MODE=true

# Kill any existing server on port 8000
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
sleep 1

echo "=== MailTrace — Email Forensic Intelligence Platform ==="
echo ""
echo "Starting backend on http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
