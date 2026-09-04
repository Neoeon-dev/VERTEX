"""Shared test fixtures.

Uses an in-memory SQLite database so tests run without PostgreSQL.
"""
from __future__ import annotations

import os

# Force SQLite before any app imports that read database_url
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
# Disable .env file loading during tests
os.environ["DEMO_MODE"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base, get_db
from app.main import app

# Create a fresh engine + tables for the test session
_test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestSession = sessionmaker(bind=_test_engine, autocommit=False, autoflush=False)


def _override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _create_tables():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture()
def client():
    return TestClient(app)


# ── Sample .eml fixtures ────────────────────────────────────────────

SAMPLE_EML = b"""\
From: John Doe <john@example.com>
To: jane@example.com
Cc: bob@example.com
Subject: Test Email
Date: Mon, 01 Jan 2024 12:00:00 +0000
Message-ID: <test-001@example.com>
Reply-To: reply@example.com
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"

Hello, this is a test email body.
"""

SAMPLE_EML_MULTIPART = b"""\
From: Sender <sender@evil.com>
To: victim@target.com
Subject: Important Invoice
Date: Tue, 02 Jan 2024 14:30:00 +0000
Message-ID: <test-002@evil.com>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset="utf-8"

Please see the attached invoice.

--boundary123
Content-Type: application/pdf
Content-Disposition: attachment; filename="invoice.pdf"
Content-Transfer-Encoding: base64

JVBERi0xLjAKMSAwIG9iago=
--boundary123--
"""

SAMPLE_EML_HEADERS_ONLY = b"""\
From: Attacker <attacker@phish.net>
To: ceo@company.com
Subject: Urgent: Wire Transfer Required
Received: from mail.phish.net (phish.net [192.168.1.1])
        by mx.company.com (8.14.4/8.14.4) with ESMTP id abc123
        for <ceo@company.com>; Mon, 01 Jan 2024 12:00:00 +0000
Received: from unknown (HELO local) (10.0.0.1)
        by mail.phish.net with SMTP; Mon, 01 Jan 2024 11:59:00 +0000
Authentication-Results: mx.company.com;
        spf=fail (domain of attacker@phish.net does not designate 192.168.1.1 as permitted sender);
        dkim=none header.d=phish.net;
        dmarc=fail (p=REJECT) header.from=phish.net
Content-Type: text/plain; charset="utf-8"

Wire the money immediately.
"""
