from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.ingest import router as ingest_router
from routers.signals import router as signals_router
from routers.trades import router as trades_router
from routers.admin import router as admin_router

from utils.logging import get_logger
from utils.db_helpers import init_db

app = FastAPI(title="Comoda Backend API", version="0.1.0")

# CORS configuration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info({"event": "startup", "message": "Initializing database and services"})
    init_db()

@app.get("/health", tags=["health"])  # Simple health check
async def health():
    return {"status": "ok"}

# Include routers
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
app.include_router(signals_router, prefix="/signals", tags=["signals"])
app.include_router(trades_router, prefix="/trades", tags=["trades"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])