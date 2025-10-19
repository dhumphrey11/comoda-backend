import os
from typing import Any, Dict, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from .logging import get_logger

logger = get_logger(__name__)

_engine: Optional[Engine] = None
_SessionLocal = None

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/comoda")


def init_db():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)  # type: ignore[assignment]
        logger.info({"event": "db_init", "message": "Database initialized"})
        # Create minimal tables if they do not exist (idempotent)
        if _engine is not None:
            with _engine.begin() as conn:
                conn.execute(text(
                """
                CREATE TABLE IF NOT EXISTS error_logs (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT NOW(),
                    context TEXT NOT NULL,
                    message TEXT NOT NULL,
                    extra JSONB
                );
                CREATE TABLE IF NOT EXISTS portfolio (
                    id SERIAL PRIMARY KEY,
                    cash_available NUMERIC DEFAULT 20000
                );
                INSERT INTO portfolio (cash_available)
                SELECT 20000 WHERE NOT EXISTS (SELECT 1 FROM portfolio);
                CREATE TABLE IF NOT EXISTS positions (
                    ticker TEXT PRIMARY KEY,
                    quantity NUMERIC NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS trades (
                    id SERIAL PRIMARY KEY,
                    ticker TEXT NOT NULL,
                    action TEXT NOT NULL,
                    quantity NUMERIC NOT NULL,
                    price NUMERIC NOT NULL,
                    executed_at TIMESTAMP DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS trade_rules (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                INSERT INTO trade_rules(key, value) VALUES
                    ('max_allocation_pct','5.0') ON CONFLICT (key) DO NOTHING;
                INSERT INTO trade_rules(key, value) VALUES
                    ('slippage_pct','0.1') ON CONFLICT (key) DO NOTHING;
                INSERT INTO trade_rules(key, value) VALUES
                    ('fees_pct','0.05') ON CONFLICT (key) DO NOTHING;
                CREATE TABLE IF NOT EXISTS market_prices (
                    ticker TEXT NOT NULL,
                    price NUMERIC NOT NULL,
                    ts TIMESTAMP DEFAULT NOW()
                );
                """
                ))


def get_db_session():
    if _SessionLocal is None:
        init_db()
    # mypy: _SessionLocal is initialized in init_db
    return _SessionLocal()  # type: ignore[operator]


async def log_error(context: str, message: str, extra: Optional[Dict[str, Any]] = None):
    logger.error({"context": context, "error": message, "extra": extra or {}})
    try:
        with get_db_session() as db:
            db.execute(
                text(
                    """
                    INSERT INTO error_logs (context, message, extra)
                    VALUES (:context, :message, :extra)
                    """
                ),
                {"context": context, "message": message, "extra": (extra or {})},
            )
            db.commit()
    except Exception as e:
        logger.error({"event": "error_log_failure", "detail": str(e)})