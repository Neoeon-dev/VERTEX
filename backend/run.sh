#!/bin/bash
# MailTrace — Quick Start (SQLite mode)
# No PostgreSQL required for local development

export DATABASE_URL="sqlite:///./mailtrace.db"
export DEMO_MODE=true

echo "=== MailTrace — Email Forensic Intelligence Platform ==="
echo ""
echo "Starting backend on http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
