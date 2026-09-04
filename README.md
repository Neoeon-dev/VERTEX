# SIH26106 — MailTrace: AI-Powered Email Threat Detection, GeoLocation & Forensic Intelligence Platform

> Analyze suspicious emails, detect phishing, and generate forensic reports with a single `.eml` upload.

---

## 🚀 User Manual / Getting Started

### What This Application Does

**MailTrace** is an email forensic intelligence platform. It helps security analysts, incident responders, and IT teams investigate suspicious emails.

**What happens after you upload an email:**

1. The `.eml` file is parsed — all headers, body text, and attachments are extracted.
2. A SHA-256 evidence hash is computed on the raw file bytes (for tamper-evident chain of custody).
3. Email authentication is checked (SPF, DKIM, DMARC) via independent DNS lookups.
4. The email relay path (Received headers) is reconstructed and analyzed for anomalies.
5. All IP addresses found in the headers are geolocated and ASN-resolved.
6. Domains are checked for brand impersonation, homoglyphs, and suspicious TLDs.
7. URLs in the body are extracted and analyzed for phishing indicators.
8. Attachments are analyzed for dangerous extensions and MIME mismatches (never executed).
9. An ML classifier (TF-IDF + Logistic Regression) categorizes the email.
10. A weighted risk engine combines all signals into a 0–100 risk score with full explainability.
11. A forensic PDF report can be generated with all findings.

**Who uses it:** Security analysts, SOC teams, incident responders, and IT administrators.

---

### Prerequisites

| Software | Required Version | Why It Is Needed | How to Verify |
|---|---|---|---|
| **Git** | Any recent version | Clone the repository | `git --version` |
| **Python** | ≥ 3.11 | Backend server and forensics engine | `python3 --version` |
| **Node.js** | ≥ 18 (LTS recommended) | Frontend build and dev server | `node --version` |
| **npm** | Comes with Node.js | Install frontend dependencies | `npm --version` |
| **Docker** | ≥ 20.10 (optional) | Run PostgreSQL database | `docker --version` |
| **Docker Compose** | ≥ 2.0 (optional) | Orchestrate services | `docker compose version` |

**Docker is optional.** You can run the backend in SQLite mode without Docker.

---

### Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

---

### Environment Setup

MailTrace uses environment variables for configuration. A `.env` file in the `backend/` directory is optional — all variables have defaults.

#### Option A: SQLite Mode (Simplest — No Docker Required)

No `.env` file needed. The provided `run.sh` script sets `DATABASE_URL` to SQLite and enables demo mode automatically.

#### Option B: PostgreSQL via Docker

Create `backend/.env` with the following:

| Variable | Required? | Purpose | Default | Example |
|---|---|---|---|---|
| `DATABASE_URL` | No | PostgreSQL connection string | `postgresql+psycopg2://mailtrace:mailtrace@localhost:5432/mailtrace` | `postgresql+psycopg2://mailtrace:mailtrace@localhost:5432/mailtrace` |
| `DEMO_MODE` | No | Enable offline demo fixtures | `false` | `true` |
| `MAX_UPLOAD_SIZE_MB` | No | Max uploaded file size in MB | `10` | `20` |
| `GEOIP_DB_DIR` | No | Directory containing GeoLite2 `.mmdb` files | `/usr/share/GeoIP` | `./data/geoip` |

> **Secrets:** Never commit passwords, API keys, or tokens to the repository. The defaults above are for local development only.

---

### Database Setup

#### Option A: SQLite (No Setup Required)

If using `run.sh`, the SQLite database file `mailtrace.db` is created automatically in `backend/` on first run. No migrations needed — tables are created at startup.

#### Option B: PostgreSQL via Docker

```bash
docker compose up -d db
```

This starts a PostgreSQL 16 container. The database is created automatically from the `docker-compose.yml` environment variables. Tables are created on backend startup (no migration step required).

Verify the database is running:

```bash
docker compose ps db
```

You should see the `db` service with status `Up`.

---

### Required Data Files

| File | Mandatory? | Purpose | How to Obtain | What Happens If Missing |
|---|---|---|---|---|
| **GeoLite2-City.mmdb** | No | IP geolocation lookups | Free from [MaxMind](https://www.maxmind.com/en/geolite2/signup). Place in `backend/data/geoip/` | IP geolocation returns `null`. All other features work normally. |
| **GeoLite2-ASN.mmdb** | No | ASN / organization lookups | Same source as above. Place in `backend/data/geoip/` | ASN data returns `null`. All other features work normally. |

Without these files, the platform runs fully functional. IP intelligence will include warnings that geolocation data is unavailable.

---

### Start the Application

#### Method 1: Quick Start with SQLite (Recommended for First-Time Users)

```bash
cd backend
bash run.sh
```

This starts the backend on port 8000 with SQLite and demo mode enabled. **No Docker required.**

Then in a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

#### Method 2: Docker Compose (Full Stack with PostgreSQL)

```bash
docker compose up --build
```

This builds and starts the backend and PostgreSQL. The frontend must be started separately (see below).

Then in a **second terminal** for the frontend:

```bash
cd frontend
npm install
npm run dev
```

#### Method 3: Manual Setup

**Terminal 1 — Database (if using PostgreSQL):**

```bash
docker compose up -d db
```

**Terminal 2 — Backend:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 — Frontend:**

```bash
cd frontend
npm install
npm run dev
```

---

### Verify the Installation

Run each of these in a new terminal after starting the application:

```bash
# 1. Backend health check
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# 2. API docs
curl -s http://localhost:8000/docs | head -5
# Expected: Swagger UI HTML (if using a browser)

# 3. Frontend
curl -s http://localhost:5173 | head -5
# Expected: HTML page with title "MailTrace — Email Forensic Intelligence"
```

Checklist:

```
✓ Database running (if PostgreSQL)
✓ Backend running on port 8000
✓ Frontend running on port 5173
✓ API health check returns {"status":"ok"}
✓ API docs accessible at http://localhost:8000/docs
```

---

### Local URLs

| Service | URL | Purpose |
|---|---|---|
| **Frontend** | `http://localhost:5173` | Web application UI |
| **Backend API** | `http://localhost:8000` | REST API |
| **API Docs (Swagger)** | `http://localhost:8000/docs` | Interactive API documentation |
| **API Docs (ReDoc)** | `http://localhost:8000/redoc` | Alternative API documentation |
| **Database** | `localhost:5432` | PostgreSQL (if using Docker) |

---

### First-Time User Workflow

#### Step 1: Open the Application

Navigate to `http://localhost:5173` in your browser. You will see the **Upload Email** page with a drag-and-drop area.

#### Step 2: Upload a `.eml` File

Click the upload area or drag a `.eml` file onto it. The file is validated (must end in `.eml`, max 10 MB).

> **Don't have a `.eml` file?** Save any suspicious email as a `.eml` file from your email client. In Gmail: open the email → three-dot menu → "Show original" → "Download Original". In Outlook: drag the email to your desktop.

#### Step 3: Wait for Parsing

The email is parsed instantly — headers, body, and attachments are extracted. You are redirected to the email detail page.

#### Step 4: Click "Run Full Analysis"

On the email detail page, click the **"Run Full Analysis"** button. This triggers all forensic modules simultaneously:

- SPF / DKIM / DMARC authentication
- Received header relay path analysis
- IP intelligence (geolocation + ASN)
- Domain intelligence (lookalikes, homoglyphs)
- URL analysis
- Attachment analysis
- ML classification
- Risk scoring

#### Step 5: Review the Results

Scroll through the collapsible sections to review:

1. **Risk Assessment** — Overall score (0–100) and level (LOW/MEDIUM/HIGH/CRITICAL)
2. **Email Metadata** — Subject, sender, recipients, SHA-256 evidence hash
3. **AI Classification** — ML prediction with probabilities and explainable signals
4. **Authentication** — SPF, DKIM, DMARC results with domain and details
5. **Received Path** — Relay hops, public/private IPs, anomalies
6. **Domain Intelligence** — Suspicious TLDs, lookalikes, homoglyphs
7. **URLs** — IP-based URLs, shorteners, suspicious paths
8. **Attachments** — Dangerous extensions, double extensions, MIME mismatches
9. **All Headers** — Every raw header in original order

---

### Dashboard Guide

#### Risk Score (0–100)

The risk score is a weighted combination of all analysis signals. It does **not** prove the email is malicious — it is an inference.

| Range | Level | Meaning |
|---|---|---|
| 0–24 | **LOW** | Few risk signals detected. Likely legitimate. |
| 25–49 | **MEDIUM** | Some suspicious indicators. Worth investigating. |
| 50–74 | **HIGH** | Multiple risk signals. Likely phishing or fraud. |
| 75–100 | **CRITICAL** | Many strong risk signals. Treat as confirmed threat. |

#### Classification

The ML classifier assigns one of four labels:

| Label | Meaning |
|---|---|
| **legitimate** | Normal business or personal email |
| **suspicious** | Some indicators but not conclusive |
| **phishing** | Strong indicators of credential theft or fraud |
| **spammer** | Unsolicited bulk email |

Each label comes with a confidence score (0–100%) and probability distribution across all classes.

#### SPF (Sender Policy Framework)

SPF checks whether the sending server is authorized to send email for the domain.

| Result | Meaning |
|---|---|
| **PASS** | The sending IP is authorized by the domain's SPF record |
| **FAIL** | The sending IP is NOT authorized — strong phishing indicator |
| **SOFTFAIL** | The sending IP is not authorized but the domain policy is permissive |
| **NONE** | No SPF record published by the domain |
| **TEMPERROR** | DNS lookup failed temporarily |

**Important:** SPF validates the *envelope sender* (Return-Path), NOT the visible From address.

#### DKIM (DomainKeys Identified Mail)

DKIM verifies a cryptographic signature attached by the sending server.

| Result | Meaning |
|---|---|
| **PASS** | Signature verified against the domain's public key |
| **FAIL** | Signature verification failed |
| **NONE** | No DKIM-Signature header found |
| **PERMERROR** | DKIM key lookup failed permanently |

#### DMARC (Domain-based Message Authentication, Reporting & Conformance)

DMARC combines SPF and DKIM results and checks alignment with the visible From domain.

| Result | Meaning |
|---|---|
| **PASS** | Either SPF or DKIM passed AND aligned with the From domain |
| **FAIL** | Neither SPF nor DKIM passed with alignment |
| **NONE** | No DMARC policy published by the From domain |

#### Received Chain

The relay path shows every mail server the email passed through. Read from bottom to top (chronological order):

- Each hop shows the source hostname, IP, protocol, and timestamp.
- **Public IPs** indicate internet infrastructure.
- **Private IPs** indicate internal corporate servers.
- **Anomalies** flagged: missing headers, non-monotonic timestamps, unusually many hops, duplicate IPs.

#### IP Intelligence

For each public IP in the relay path:

- **Geolocation** — Country, city, lat/lon (via MaxMind GeoLite2). This shows *infrastructure location*, not attacker physical location.
- **ASN** — Autonomous System Number and organization (who operates the network).

#### Domain Intelligence

Domains found in headers and body are analyzed for:

- **Suspicious TLDs** — `.xyz`, `.top`, `.club`, etc.
- **Homoglyphs** — Non-Latin characters that look like Latin letters (Cyrillic tricks).
- **Lookalike domains** — Levenshtein distance comparison against known brands.
- **Punycode** — Internationalized domain names that may hide the real domain.

#### URL Analysis

URLs extracted from the email body are checked for:

- **IP-based URLs** — Using an IP address instead of a domain name.
- **URL shorteners** — `bit.ly`, `tinyurl.com`, `t.co`, etc.
- **Suspicious paths** — `/login`, `/verify`, `/signin`, `/password`.
- **Excessive subdomains** — More than 3 levels of subdomains.
- **Punycode** — Internationalized domain names in URLs.

#### Attachments

Attachments are analyzed **without executing them**:

- **Dangerous extensions** — `.exe`, `.scr`, `.vbs`, `.bat`, `.ps1`, etc.
- **Double extensions** — `invoice.pdf.exe` (disguised executables).
- **MIME mismatches** — MIME type doesn't match the file extension.
- **SHA-256** — Each attachment's hash is recorded for evidence tracking.

#### Correlation Graph

The correlation graph shows relationships between emails, senders, domains, IPs, and cases. It reveals:

- Shared infrastructure across multiple emails (same IP or domain).
- Campaign patterns (multiple emails from the same sender or domain).
- Case associations.

#### Evidence & Chain of Custody

Every email's evidence integrity is maintained through:

- **SHA-256 hash** — Computed on the raw uploaded bytes before any parsing.
- **Evidence chain** — Append-only hash chain recording every action (upload, analyze, export).
- **Audit log** — Immutable log of all system actions with hash-chain integrity.

You can verify chain integrity via:
- `GET /api/evidence/verify/{email_id}` — Verify evidence chain for a specific email.
- `POST /api/audit/verify` — Verify the global audit log integrity.

---

### How to Analyze a Suspicious Email

> **Scenario:** You receive an email claiming to be from your bank, asking you to "verify your account immediately."

#### Step 1: Preserve the Original

- Do NOT delete the email.
- Save it as a `.eml` file (use "Download Original" or "Show Original" in your email client).
- Do NOT modify the file in any way.

#### Step 2: Upload to MailTrace

1. Open `http://localhost:5173`.
2. Drag the `.eml` file onto the upload area.
3. Wait for parsing to complete.

#### Step 3: Run Full Analysis

Click "Run Full Analysis" on the email detail page.

#### Step 4: Review Authentication

Check SPF, DKIM, and DMARC. If all are FAIL, the email is very likely spoofed.

#### Step 5: Check the Sender Identity

Look at the "From" address and "Sender Name." If the display name says "Bank of America" but the email address is `security@b4nk-secure.xyz`, that's a major red flag.

#### Step 6: Review the Relay Path

Check the Received headers. Unusual servers or many hops may indicate the email was routed through attacker-controlled infrastructure.

#### Step 7: Review IP and Domain Intelligence

Look for geolocation warnings, suspicious TLDs, lookalike domains, or homoglyphs.

#### Step 8: Check URLs

If the email contains links, review them. IP-based URLs and shorteners are suspicious.

#### Step 9: Check Attachments

Dangerous extensions (`.exe`, `.scr`) or double extensions (`document.pdf.exe`) are strong indicators of malware.

#### Step 10: Review Risk Factors

The risk engine shows exactly which signals contributed to the score and how much.

#### Step 11: Check Related Cases

If you have uploaded multiple suspicious emails, use the correlation graph to find shared infrastructure.

#### Step 12: Generate a Forensic Report

Download the PDF report from `GET /api/reports/{email_id}/pdf` for documentation and evidence preservation.

---

### Evidence Handling Instructions

> **IMPORTANT — When using MailTrace for forensic investigation:**

1. **Preserve the original `.eml` file.** The SHA-256 hash is computed on the raw bytes.
2. **Do NOT edit the file before upload.** Any modification changes the evidence hash.
3. **Record the evidence SHA-256** displayed on the email detail page.
4. **Record the email ID** (`#N`) for case tracking.
5. **Do NOT execute suspicious attachments.** MailTrace stores them inertly (never executed or rendered).
6. **Do NOT click suspicious URLs.** The platform analyzes them safely without visiting them.
7. **Verify chain integrity** using `POST /api/audit/verify` and `GET /api/evidence/verify/{email_id}`.

MailTrace preserves evidence through an append-only hash chain. Every action (upload, analysis, export) is recorded with a cryptographic hash linking to the previous entry. Tampering with any record breaks the chain.

---

### Running the Offline Demo

MailTrace includes a demo mode that replaces external intelligence lookups with deterministic fixtures.

**To enable demo mode:**

1. Set `DEMO_MODE=true` in your environment or `.env` file.
2. Or use `bash run.sh` in the `backend/` directory (sets it automatically).

**What demo mode does:**

- Core parsing, authentication (SPF/DKIM/DMARC), and ML classification work normally.
- GeoIP lookups return stub data (no MaxMind database required).
- Domain intelligence and URL analysis work normally.
- Risk scoring works normally.

**What you need:**

- The backend server running.
- Any `.eml` file to upload.

**How it differs from live mode:**

- No external DNS queries for SPF/DKIM/DMARC (uses header claims).
- No GeoIP database required.
- All other features work identically.

---

### Stopping the Application

#### If using `run.sh`:

Press `Ctrl+C` in the terminal running the backend.

#### If using Docker Compose:

```bash
docker compose down
```

This stops all containers but **preserves** the database data.

To also delete the database volume:

```bash
docker compose down -v
```

> ⚠️ **Warning:** `docker compose down -v` deletes the PostgreSQL data volume. All analyzed emails will be lost.

#### If running manually:

Press `Ctrl+C` in each terminal (backend, then frontend).

---

### Restarting the Application

```bash
# Quick start (SQLite mode)
cd backend
bash run.sh

# Then in another terminal
cd frontend
npm run dev
```

```bash
# Docker Compose
docker compose up

# Then in another terminal
cd frontend
npm run dev
```

No rebuild is needed unless you changed dependencies or code.

---

### Updating the Application

```bash
git pull

# Backend — reinstall dependencies if requirements changed
cd backend
pip install -r requirements.txt

# Frontend — reinstall if package.json changed
cd frontend
npm install
```

No database migration step is required — tables are created automatically at startup.

---

### Troubleshooting

#### Backend Won't Start

**Symptom:** `ModuleNotFoundError` or import errors on startup.

**Cause:** Missing Python dependencies.

**Fix:**
```bash
cd backend
pip install -r requirements.txt
```

**Verification:** `python -c "import fastapi; print('OK')"`

---

#### Port Already in Use (Address already in use)

**Symptom:** `[Errno 98] Address already in use` when starting the server.

**Cause:** Another process is using port 8000.

**Fix:**
```bash
# Kill whatever is using port 8000
lsof -ti :8000 | xargs kill -9
# Or use run.sh which does this automatically
bash run.sh
```

---

#### Frontend Won't Start

**Symptom:** `npm run dev` fails with errors.

**Cause:** Missing Node.js dependencies.

**Fix:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

**Verification:** Open `http://localhost:5173` — you should see the MailTrace UI.

---

#### Database Connection Failure

**Symptom:** `sqlalchemy.exc.OperationalError: could not connect to server` or `psycopg2.OperationalError`.

**Cause:** PostgreSQL is not running or `DATABASE_URL` is wrong.

**Fix:**
1. If using Docker: `docker compose up -d db`
2. If using SQLite: set `DATABASE_URL=sqlite:///./mailtrace.db`
3. Check the connection string in your `.env` file.

**Verification:** `docker compose ps db` should show status `Up`.

---

#### Stale Python Cache (old code running after edits)

**Symptom:** Bug fixes don't take effect even after editing source files. Server still shows old behavior.

**Cause:** Python's `__pycache__` directories contain compiled bytecode from previous runs.

**Fix:**
```bash
# Delete all Python cache files
find . -name "__pycache__" -exec rm -rf {} +
# Restart the server
bash run.sh
```

This is handled automatically by `run.sh`.

---

#### Docker Problems

**Symptom:** `docker compose up` fails.

**Fix:**
1. Ensure Docker is running: `docker info`
2. Rebuild: `docker compose up --build`
3. Check logs: `docker compose logs db` or `docker compose logs backend`

---

#### Missing Environment Variable

**Symptom:** `pydantic_settings.ValidationError` on backend startup.

**Cause:** A required environment variable is not set.

**Fix:** Create `backend/.env` with the required variables. See the [Environment Configuration](#environment-configuration) section.

---

#### Missing GeoIP Database

**Symptom:** IP intelligence returns `null` for geolocation. Logs show "GeoLite2-City not found."

**Cause:** MaxMind GeoLite2 `.mmdb` files are not present.

**Fix:** Download from [MaxMind](https://www.maxmind.com/en/geolite2/signup) and place in `backend/data/geoip/`.

**Impact:** All other features work. Only IP geolocation and ASN data are missing.

---

#### Upload Failure

**Symptom:** `400` or `413` error when uploading.

**Fix:**
- Ensure the file ends in `.eml`.
- Ensure the file is under 10 MB (configurable via `MAX_UPLOAD_SIZE_MB`).

---

#### CORS Issue / API Unreachable from Frontend

**Symptom:** Frontend shows network errors; browser console shows CORS errors.

**Cause:** Frontend is not proxying to the backend.

**Fix:** The Vite config (`frontend/vite.config.js`) proxies `/api` and `/health` to `http://localhost:8000`. Ensure the backend is running on port 8000.

---

#### PDF Generation Failure

**Symptom:** `GET /api/reports/{id}/pdf` returns HTML instead of PDF.

**Cause:** `weasyprint` is not installed.

**Fix:**
```bash
pip install weasyprint
```

**Impact:** The endpoint returns an HTML version of the report as a fallback.

---

#### Dependency Installation Failure

**Symptom:** `pip install` or `npm install` fails.

**Fix:**
- Ensure you have the correct Python/Node.js version.
- For Python: try `pip install --upgrade pip` first.
- For Node.js: try `rm -rf node_modules && npm install`.

---

---

## 👨‍💻 Developer Quick Start

### Repository Architecture

```
├── backend/                  # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app, router registration, lifespan
│   │   ├── config.py         # Pydantic Settings (env vars)
│   │   ├── db.py             # SQLAlchemy engine, session, Base
│   │   ├── models.py         # ORM models (Email, Case, AuditLog, EvidenceChain, etc.)
│   │   ├── utils.py          # Shared utilities
│   │   ├── schemas/          # Pydantic response schemas
│   │   ├── routers/          # API endpoint modules
│   │   ├── forensics/        # Analysis engines (SPF, DKIM, DMARC, IP, domain, URL, etc.)
│   │   ├── ml/               # ML classifier (TF-IDF + Logistic Regression)
│   │   └── parsers/          # MIME email parser
│   ├── tests/                # pytest test suite
│   ├── data/geoip/           # GeoLite2 database files (user-provided)
│   ├── requirements.txt      # Python dependencies
│   ├── pyproject.toml        # Project metadata + pytest config
│   ├── Dockerfile            # Backend Docker image
│   └── run.sh                # Quick-start script (SQLite mode)
├── frontend/                 # React/Vite frontend
│   ├── src/
│   │   ├── App.jsx           # Router, sidebar, layout
│   │   ├── api.js            # Axios API client
│   │   ├── index.css         # Tailwind CSS theme
│   │   └── pages/            # UploadPage, EmailListPage, EmailDetailPage
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite config with API proxy
│   └── Dockerfile            # (placeholder)
├── docker-compose.yml        # PostgreSQL + Backend orchestration
└── README.md
```

### Backend Development

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-env httpx  # test dependencies
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Adding a new forensics module:**
1. Create `app/forensics/your_module.py` with your analysis logic.
2. Create a router in `app/routers/your_router.py`.
3. Register it in `app/main.py` via `app.include_router(...)`.

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` and `/health` to `http://localhost:8000`.

### Running Tests

```bash
cd backend
pytest -v
```

Tests use an in-memory SQLite database — no PostgreSQL or external services required.

### Adding New API Endpoints

1. Define a Pydantic response model in `backend/app/schemas/` or inline in the router.
2. Create a new router or add to an existing one in `backend/app/routers/`.
3. Register the router in `backend/app/main.py`.
4. Write tests in `backend/tests/`.

---

## 📖 Project Overview

MailTrace is an AI-powered email forensic intelligence platform built for [Smart India Hackathon 2026](https://sih.gov.in/) (Problem Statement SIH26106). It provides:

- Complete email parsing with evidence chain of custody
- Independent SPF/DKIM/DMARC authentication
- Email relay path reconstruction and anomaly detection
- IP geolocation and ASN intelligence
- Domain lookalike and homoglyph detection
- URL phishing indicator analysis
- Attachment risk analysis (without execution)
- ML-based threat classification with explainable signals
- Weighted multi-signal risk scoring with full breakdown
- Correlation graph for campaign detection
- Forensic PDF report generation
- Append-only audit log with hash-chain integrity

---

## 🎯 Problem Statement

Email-based threats (phishing, BEC, spear-phishing) are the #1 attack vector. Existing tools often:

- Rely on external reputation services that may be unavailable
- Don't provide explainable analysis
- Don't preserve forensic evidence properly
- Can't correlate multiple incidents

---

## 💡 Proposed Solution

MailTrace provides a self-contained forensic platform that:

- Performs all analysis locally (no external API dependencies for core features)
- Provides explainable risk scoring with FACT → OBSERVATION → INFERENCE → CONFIDENCE
- Preserves evidence through SHA-256 hashing and append-only hash chains
- Correlates multiple emails to detect campaigns
- Works in offline/demo mode for air-gapped environments

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **MIME Parsing** | Full header extraction, body parsing, attachment extraction |
| **Evidence Integrity** | SHA-256 on raw bytes, append-only hash chain |
| **SPF/DKIM/DMARC** | Independent DNS-based authentication verification |
| **Received Path Analysis** | Relay reconstruction, anomaly detection |
| **IP Intelligence** | GeoLite2 geolocation, ASN resolution |
| **Domain Intelligence** | Lookalike detection, homoglyph analysis, TLD checking |
| **URL Analysis** | IP URLs, shorteners, suspicious paths, punycode |
| **Attachment Analysis** | Dangerous extensions, double extensions, MIME mismatches |
| **ML Classification** | TF-IDF + Logistic Regression with explainable signals |
| **Risk Engine** | Weighted 8-category scoring (0–100) with full breakdown |
| **Correlation Graph** | NetworkX-based campaign and shared-infrastructure detection |
| **Audit Log** | Immutable append-only log with hash-chain integrity |
| **PDF Reports** | Forensic report generation (HTML fallback) |

---

## 🏗️ System Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend API   │────▶│  PostgreSQL  │
│  React/Vite  │     │   FastAPI       │     │  (or SQLite) │
│  :5173       │     │   :8000         │     │  :5432       │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │  Forensics  │
                    │  Engine     │
                    └─────────────┘
```

The frontend communicates with the backend via a REST API. The Vite dev server proxies `/api` requests to the backend. The backend handles all analysis, ML inference, and database operations.

---

## 📧 Email Analysis Pipeline

```
.eml Upload
    │
    ▼
SHA-256 Evidence Hash (computed on raw bytes)
    │
    ▼
MIME Parsing (headers, body, attachments)
    │
    ▼
┌────────────────────────────────────────────┐
│           Parallel Analysis Modules         │
├────────────┬───────────┬───────────────────┤
│ SPF/DKIM/  │ Received  │ IP Intelligence   │
│ DMARC      │ Headers   │ (GeoIP + ASN)     │
├────────────┼───────────┼───────────────────┤
│ Domain     │ URL       │ Attachment        │
│ Intelligence│ Analysis │ Analysis          │
├────────────┴───────────┴───────────────────┤
│         ML Classification                   │
├─────────────────────────────────────────────┤
│         Risk Engine (weighted scoring)       │
└─────────────────────────────────────────────┘
    │
    ▼
Results + Forensic Report
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version |
|---|---|---|
| **Frontend** | React | 19.x |
| **Frontend Build** | Vite | 8.x |
| **Styling** | Tailwind CSS | 4.x |
| **HTTP Client** | Axios | 1.20.x |
| **Routing** | React Router | 7.x |
| **Backend** | FastAPI | 0.141.x |
| **ORM** | SQLAlchemy | 2.0.x |
| **Database** | PostgreSQL | 16 |
| **Database (dev)** | SQLite | Built-in |
| **ML** | scikit-learn | Latest |
| **ML Persistence** | joblib | Latest |
| **Graph** | NetworkX | Latest |
| **DNS** | dnspython | Latest |
| **DKIM** | dkimpy | Latest |
| **GeoIP** | geoip2 | Latest |
| **PDF** | WeasyPrint (optional) | Latest |
| **Validation** | Pydantic | v2 |
| **Config** | pydantic-settings | Latest |
| **Tests** | pytest + httpx | Latest |

---

## 📁 Repository Structure

| Path | Description |
|---|---|
| `backend/app/main.py` | FastAPI application entry point |
| `backend/app/config.py` | Environment-based configuration |
| `backend/app/db.py` | Database engine and session factory |
| `backend/app/models.py` | SQLAlchemy ORM models |
| `backend/app/routers/` | API endpoint modules (9 routers) |
| `backend/app/forensics/` | Analysis engines (11 modules) |
| `backend/app/ml/` | ML classifier |
| `backend/app/parsers/` | MIME email parser |
| `backend/app/schemas/` | Pydantic response schemas |
| `backend/tests/` | Test suite (8 test files) |
| `frontend/src/pages/` | React page components |
| `frontend/src/api.js` | API client functions |
| `frontend/vite.config.js` | Vite configuration with proxy |

---

## 📚 Module Reference

| Module | Path | Purpose |
|---|---|---|
| `mime_parser` | `backend/app/parsers/mime_parser.py` | Parse `.eml` bytes into structured data |
| `spf_analyzer` | `backend/app/forensics/spf_analyzer.py` | SPF DNS verification |
| `dkim_analyzer` | `backend/app/forensics/dkim_analyzer.py` | DKIM signature verification |
| `dmarc_analyzer` | `backend/app/forensics/dmarc_analyzer.py` | DMARC policy evaluation |
| `received_analyzer` | `backend/app/forensics/received_analyzer.py` | Received header relay reconstruction |
| `ip_intelligence` | `backend/app/forensics/ip_intelligence.py` | GeoIP + ASN lookup |
| `domain_intel` | `backend/app/forensics/domain_intel.py` | Domain lookalike/homoglyph detection |
| `url_analyzer` | `backend/app/forensics/url_analyzer.py` | URL phishing indicator analysis |
| `attachment_analyzer` | `backend/app/forensics/attachment_analyzer.py` | Attachment risk analysis |
| `risk_engine` | `backend/app/forensics/risk_engine.py` | Weighted multi-signal scoring |
| `evidence` | `backend/app/forensics/evidence.py` | Evidence hash chain + audit log |
| `correlation` | `backend/app/forensics/correlation.py` | NetworkX correlation graph |
| `classifier` | `backend/app/ml/classifier.py` | TF-IDF + Logistic Regression classifier |

---

## 🔧 Backend Architecture

The backend follows a layered architecture:

1. **Routers** (`app/routers/`) — HTTP endpoints, request validation, response formatting.
2. **Forensics** (`app/forensics/`) — Pure analysis logic, no HTTP concerns.
3. **ML** (`app/ml/`) — Machine learning classification with synthetic training data.
4. **Parsers** (`app/parsers/`) — MIME/RFC-822 email parsing.
5. **Models** (`app/models.py`) — SQLAlchemy ORM models for persistence.
6. **Config** (`app/config.py`) — Environment-based settings via pydantic-settings.

All forensics modules are stateless and can be called independently. The risk engine orchestrates all modules and produces the final score.

---

## 🎨 Frontend Architecture

The frontend is a single-page React application with three pages:

1. **UploadPage** (`/`) — Drag-and-drop `.eml` upload with validation.
2. **EmailListPage** (`/emails`) — Table of all analyzed emails (newest first).
3. **EmailDetailPage** (`/emails/:id`) — Full analysis results with collapsible sections.

The detail page triggers three parallel API calls when "Run Full Analysis" is clicked:
- `POST /api/emails/{id}/analyze-full` — Complete forensic pipeline
- `POST /api/emails/{id}/classify` — ML classification
- `POST /api/emails/{id}/risk` — Risk assessment

---

## 🗄️ Database Architecture

### Tables

| Table | Purpose |
|---|---|
| `cases` | Investigation cases |
| `emails` | Uploaded email records with metadata |
| `email_headers` | All headers in original order |
| `attachments` | Attachment metadata and inert bytes |
| `email_authentication_results` | SPF/DKIM/DMARC analysis results |
| `audit_log` | Append-only audit trail |
| `evidence_chain` | Evidence hash chain entries |

Tables are created automatically at startup via `Base.metadata.create_all()`.

---

## 📡 API Reference

### Email Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/emails/analyze` | Upload and parse a `.eml` file |
| `GET` | `/api/emails` | List analyzed emails |
| `GET` | `/api/emails/{id}` | Get email detail |

### Analysis Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/emails/{id}/authentication` | Run SPF/DKIM/DMARC analysis |
| `GET` | `/api/emails/{id}/authentication` | Get authentication results |
| `POST` | `/api/emails/{id}/received` | Analyze Received headers |
| `GET` | `/api/emails/{id}/received` | Get relay path analysis |
| `POST` | `/api/emails/{id}/ip-intel` | Analyze IP addresses |
| `GET` | `/api/emails/{id}/ip-intel` | Get IP intelligence |
| `POST` | `/api/emails/{id}/classify` | Run ML classification |
| `GET` | `/api/emails/{id}/classify` | Get classification results |
| `POST` | `/api/emails/{id}/risk` | Compute risk assessment |
| `GET` | `/api/emails/{id}/risk` | Get risk assessment |
| `POST` | `/api/emails/{id}/analyze-full` | Run complete forensic pipeline |
| `GET` | `/api/emails/{id}/analyze-full` | Get full analysis results |

### Case & Audit Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/cases` | Create a case |
| `GET` | `/api/cases` | List cases |
| `GET` | `/api/cases/{id}` | Get case detail |
| `PUT` | `/api/cases/{id}` | Update a case |
| `POST` | `/api/cases/{id}/emails/{email_id}` | Assign email to case |
| `GET` | `/api/cases/{id}/emails` | List emails in case |
| `GET` | `/api/audit` | List audit log entries |
| `POST` | `/api/audit/verify` | Verify audit log integrity |
| `GET` | `/api/evidence/verify/{email_id}` | Verify evidence chain |

### Graph & Report Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/graph/email/{id}` | Add email to correlation graph |
| `GET` | `/api/graph` | Get full correlation graph |
| `GET` | `/api/graph/shared` | Find shared infrastructure |
| `GET` | `/api/reports/{id}/pdf` | Generate forensic PDF report |

### Utility Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |

---

## 🔍 Email Forensics

### SPF / DKIM / DMARC

MailTrace performs **independent** verification of email authentication:

- **SPF:** Extracts the envelope sender domain from Return-Path, looks up the DNS TXT record, and evaluates the connecting IP against the record.
- **DKIM:** Parses DKIM-Signature headers, looks up the public key, and performs cryptographic verification when raw bytes are available.
- **DMARC:** Evaluates SPF and DKIM results for alignment with the visible From domain, then checks the domain's DMARC policy.

### Header Forensics

Received headers are parsed into structured hops showing:
- Source/destination hostnames and IPs
- Protocol (ESMTP, SMTP, etc.)
- Timestamps
- Anomaly indicators (missing data, duplicate IPs, non-monotonic timestamps)

### IP & Geolocation

Public IPs are resolved via MaxMind GeoLite2:
- Country, region, city, lat/lon, accuracy radius
- ASN, organization, network range
- Private/reserved IP classification

### Domain Intelligence

Domains are checked for:
- Brand impersonation via Levenshtein distance
- Homoglyph detection (Cyrillic, fullwidth characters)
- Punycode / internationalized domain names
- Suspicious TLDs (`.xyz`, `.top`, `.club`, etc.)

### URL Analysis

URLs extracted from body text and HTML are analyzed for:
- IP-based URLs (no domain name)
- URL shorteners
- Suspicious path patterns (`/login`, `/verify`, etc.)
- Excessive subdomains
- Punycode domains

### Attachment Analysis

Attachments are analyzed **without execution**:
- Dangerous extensions (`.exe`, `.scr`, `.vbs`, `.bat`, etc.)
- Double extensions (`document.pdf.exe`)
- MIME type mismatches
- SHA-256 hash for evidence tracking

---

## 🤖 AI / ML

The classifier uses **TF-IDF vectorization** + **Logistic Regression** trained on synthetic data (4 classes: legitimate, suspicious, phishing, spammer).

**Explainable signals:**
- `urgency_language` — Presence of urgent/pressure words
- `credential_request` — Requests for passwords or login info
- `payment_request` — Wire transfer or payment demands
- `suspicious_url` — IP-based URLs or many URLs
- `impersonation` — Display name vs email address mismatch
- `authentication_anomalies` — SPF/DKIM failures

---

## 📊 Risk Scoring

The risk engine combines **8 weighted categories** into a 0–100 score:

| Category | Weight | Signals |
|---|---|---|
| ML Classification | 25% | Model prediction, confidence, explainable signals |
| Authentication | 20% | SPF, DKIM, DMARC failures |
| Identity Mismatch | 10% | Display name mismatch, Reply-To spoofing |
| Domain Intelligence | 10% | Homoglyphs, suspicious TLDs, lookalikes |
| URL Analysis | 10% | IP URLs, shorteners, suspicious paths |
| Attachment Risk | 10% | Dangerous extensions, double extensions |
| Header Anomalies | 10% | Missing headers, timestamp anomalies |
| Infrastructure | 5% | GeoIP warning signals |

Every contribution is logged with: **category → signal → raw value → weight → contribution → description → confidence level**.

---

## 🔗 Correlation Graph

Built with NetworkX, the graph tracks relationships between:
- **Nodes:** Email, Sender, Domain, IP, ASN, URL, Case
- **Edges:** SENT_FROM, ROUTED_THROUGH, RESOLVES_TO, HOSTED_BY, LINKS_TO, IMPERSONATES, PART_OF_CASE

The graph reveals shared infrastructure across multiple emails (same IP or domain used by different campaigns).

---

## 📋 Evidence & Chain of Custody

- **SHA-256** computed on raw uploaded bytes BEFORE parsing.
- **Evidence chain** entries record every action (uploaded, analyzed, exported, assigned_to_case).
- **Audit log** records all system actions with hash-chain integrity.
- Chain integrity can be verified via API endpoints.

---

## 🔒 Security / Threat Model

- Every uploaded email is treated as **hostile input**.
- Attachments are stored **inertly** — never executed or rendered.
- URLs are analyzed but **never visited**.
- File size is bounded by `MAX_UPLOAD_SIZE_MB` (default 10 MB).
- The parser handles malformed MIME gracefully.
- No user authentication is currently implemented (open access).

---

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg2://mailtrace:mailtrace@localhost:5432/mailtrace` | Database connection string |
| `DEMO_MODE` | `false` | Enable offline demo fixtures |
| `MAX_UPLOAD_SIZE_MB` | `10` | Maximum upload file size |
| `GEOIP_DB_DIR` | `/usr/share/GeoIP` | GeoLite2 database directory |

---

## 🐳 Docker Architecture

```yaml
services:
  db:        # PostgreSQL 16 on port 5432
  backend:   # FastAPI on port 8000 (depends on db)
```

The frontend is NOT containerized — it runs via `npm run dev` locally.

---

## 🧪 Testing

```bash
cd backend
pytest -v
```

**Test files:**

| File | Coverage |
|---|---|
| `test_email_api.py` | Upload, parsing, retrieval, validation |
| `test_authentication.py` | SPF/DKIM/DMARC analysis |
| `test_received.py` | Received header parsing |
| `test_ip_intel.py` | IP intelligence |
| `test_domain_url_attachment.py` | Domain, URL, attachment analysis |
| `test_ml.py` | ML classification |
| `test_risk_engine.py` | Risk scoring engine |
| `test_day12_13.py` | Correlation graph, evidence chain, cases, audit |

Tests use an **in-memory SQLite** database — no external services required.

---

## 🎬 Demo Guide

### Preparing a Demo

1. Start the application: `bash backend/run.sh`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:5173`
4. Upload a suspicious `.eml` file
5. Click "Run Full Analysis"
6. Walk through each section explaining the findings
7. Download the PDF report

### Demo Talking Points

- **Evidence integrity:** "Notice the SHA-256 hash — this proves the file hasn't been tampered with."
- **Authentication:** "SPF/DKIM/DMARC are checked independently via DNS, not just trusting what the email claims."
- **Explainable AI:** "The ML model doesn't just say 'phishing' — it shows exactly which signals (urgency, credential request, impersonation) contributed to the classification."
- **Risk scoring:** "The 0–100 score combines 8 categories with transparent weights. You can see exactly why each point was added."
- **Chain of custody:** "Every action is logged in an append-only hash chain. You can verify integrity at any time."

---

## 📦 Sample Data

No sample `.eml` files are included in the repository. To test the application:

1. Save a suspicious email as `.eml` from your email client.
2. Or export the test fixtures from `backend/tests/conftest.py` (SAMPLE_EML, SAMPLE_EML_MULTIPART, SAMPLE_EML_HEADERS_ONLY).

---

## 📋 SIH Requirement Mapping

| Requirement | Implementation |
|---|---|
| Email parsing | `parsers/mime_parser.py` — Full MIME/RFC-822 parsing |
| SPF/DKIM/DMARC | `forensics/spf_analyzer.py`, `dkim_analyzer.py`, `dmarc_analyzer.py` |
| Header forensics | `forensics/received_analyzer.py` — Relay path reconstruction |
| IP geolocation | `forensics/ip_intelligence.py` — MaxMind GeoLite2 |
| Domain intelligence | `forensics/domain_intel.py` — Lookalike, homoglyph detection |
| URL analysis | `forensics/url_analyzer.py` — Phishing indicator detection |
| Attachment analysis | `forensics/attachment_analyzer.py` — Risk without execution |
| ML classification | `ml/classifier.py` — TF-IDF + Logistic Regression |
| Risk scoring | `forensics/risk_engine.py` — 8-category weighted scoring |
| Correlation | `forensics/correlation.py` — NetworkX graph |
| Evidence integrity | `forensics/evidence.py` — Hash chain + audit log |
| Case management | `routers/cases.py` — CRUD + email assignment |
| Forensic reports | `routers/correlation.py` — PDF/HTML report generation |

---

## 📊 Project Status

**Version:** 0.1.1 (Stable)

Core features implemented:
- ✅ Email parsing and storage
- ✅ SPF/DKIM/DMARC analysis
- ✅ Received header reconstruction
- ✅ IP geolocation and ASN
- ✅ Domain intelligence
- ✅ URL analysis (including HTML `src` attribute extraction)
- ✅ Attachment analysis
- ✅ ML classification
- ✅ Risk scoring
- ✅ Correlation graph
- ✅ Evidence chain
- ✅ Audit log
- ✅ Case management
- ✅ Forensic reports
- ✅ Frontend UI
- ✅ Test suite (158 tests)
- ✅ Multi-header Received handling
- ✅ Graceful error handling with descriptive messages

---

## ⚠️ Limitations

- **No user authentication** — the platform is open access.
- **Synthetic ML training data** — the classifier is trained on hand-crafted examples, not real email datasets.
- **GeoIP accuracy** — geolocation shows infrastructure location, not attacker physical location.
- **SPF evaluation is simplified** — complex `include:` chains and IPv6 are not fully supported.
- **No real-time threat feeds** — domain/IP reputation relies on local analysis only.
- **PDF generation requires WeasyPrint** — falls back to HTML if not installed.
- **No Docker frontend container** — frontend runs via `npm run dev` only.

---

## 🗺️ Future Roadmap

- User authentication and role-based access control
- Real labeled training data for the ML classifier
- Alembic database migrations
- Real-time threat intelligence feeds
- Improved SPF evaluator with full `include:` chain support
- IPv6 support
- Batch email analysis
- Webhook notifications
- Export to SIEM formats (CEF, LEEF)
- Container orchestration for production deployment

---

## 🧩 Engineering Decisions

| Decision | Rationale |
|---|---|
| **SQLite for dev mode** | Zero-config local development. No Docker required. |
| **PostgreSQL for production** | ACID compliance, concurrent access, JSON support. |
| **Synthetic ML data** | Enables working demo without real email datasets. |
| **GeoIP as optional** | Platform works without MaxMind — no mandatory external dependency. |
| **Hash chain for evidence** | Append-only with cryptographic verification. No blockchain overhead. |
| **WeasyPrint for PDF** | Pure Python, no wkhtmltopdf dependency. Falls back to HTML gracefully. |
| **Vite proxy for API** | Avoids CORS issues in development. Production would use nginx reverse proxy. |
| **Defensive list handling** | `get_headers_dict()` returns lists for duplicate headers; all consumers handle both `str` and `list[str]`. |
| **try/except on all analysis endpoints** | Prevents raw 500 errors; returns descriptive error messages for debugging. |

---

## 📝 Changelog

### v0.1.1 (September 2026)

**Bug Fixes:**
- Fixed `TypeError` in SPF analyzer when emails have multiple `Received` headers (header values returned as `list` instead of `str`)
- Fixed URL extraction from HTML — `<img src="...">` URLs were never extracted due to a bug searching the regex pattern instead of HTML content
- Added error handling with descriptive messages on `analyze-full`, `risk`, and `classify` endpoints (previously returned generic `500 Internal Server Error`)

**Improvements:**
- Updated FastAPI 0.115.0 → 0.141.1, Starlette 0.38.6 → 1.6.0, Uvicorn 0.30.6 → 0.52.4 (fixed 57+ deprecation warnings)
- `run.sh` now auto-clears `__pycache__` and kills stale processes on startup
- All 158 tests passing with zero functional warnings

### v0.1.0 (Initial Release)
- Core email forensics pipeline
- SPF/DKIM/DMARC analysis
- ML classification with explainable signals
- Risk scoring engine
- Correlation graph
- Evidence chain of custody
- Forensic PDF reports
- React frontend with full analysis dashboard

---

## 📍 File Locator

| File | Purpose |
|---|---|
| `backend/app/main.py` | Application entry point |
| `backend/app/config.py` | Configuration (env vars) |
| `backend/app/db.py` | Database setup |
| `backend/app/models.py` | ORM models |
| `backend/app/routers/*.py` | API endpoints (10 modules) |
| `backend/app/forensics/*.py` | Analysis engines (11 modules) |
| `backend/app/ml/classifier.py` | ML classifier |
| `backend/app/parsers/mime_parser.py` | Email parser |
| `backend/tests/conftest.py` | Test fixtures |
| `frontend/src/App.jsx` | Frontend app shell |
| `frontend/src/api.js` | API client |
| `frontend/src/pages/*.jsx` | UI pages (3) |
| `frontend/vite.config.js` | Vite + proxy config |
| `docker-compose.yml` | Docker services |
| `backend/run.sh` | Quick-start script |

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Write tests for new functionality.
4. Ensure all tests pass: `pytest -v`.
5. Submit a pull request.

---

## 📄 License

This project was developed for **Smart India Hackathon 2026** (SIH26106). License terms are subject to SIH competition rules.
