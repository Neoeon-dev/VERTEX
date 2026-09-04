import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import init_db
from .routers.analysis import router as analysis_router
from .routers.authentication import router as auth_router
from .routers.cases import router as cases_router
from .routers.correlation import router as correlation_router
from .routers.emails import router as emails_router
from .routers.ip_intel import router as ip_intel_router
from .routers.ml import router as ml_router
from .routers.received import router as received_router
from .routers.risk import router as risk_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s \u2014 %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="MailTrace API",
    description="AI-Powered Email Threat Detection & Forensic Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(emails_router)
app.include_router(auth_router)
app.include_router(received_router)
app.include_router(ip_intel_router)
app.include_router(ml_router)
app.include_router(risk_router)
app.include_router(cases_router)
app.include_router(correlation_router)
app.include_router(analysis_router)


@app.get("/health")
def health():
    return {"status": "ok"}
