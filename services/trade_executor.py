from typing import Dict
from utils.db_helpers import get_db_session
from sqlalchemy import text
from utils.logging import get_logger

logger = get_logger(__name__)

class TradeExecutor:
    async def execute_trade(self, ticker: str, action: str, quantity: float) -> Dict:
        """Execute paper trades applying rules from Cloud SQL, and update portfolio."""
        with get_db_session() as db:
            # Fetch current portfolio and rules
            rules = db.execute(text("SELECT key, value FROM trade_rules")).fetchall()
            rules_map = {r[0]: float(r[1]) for r in rules}
            max_alloc_pct = float(rules_map.get("max_allocation_pct", 5.0))
            slippage_pct = float(rules_map.get("slippage_pct", 0.1))
            fees_pct = float(rules_map.get("fees_pct", 0.05))

            portfolio = db.execute(text("SELECT cash_available FROM portfolio LIMIT 1")).fetchone()
            cash_available = float(portfolio[0]) if portfolio else 20000.0

            # Fetch last price from a market data table (or external source placeholder)
            price_row = db.execute(text("SELECT price FROM market_prices WHERE ticker=:t ORDER BY ts DESC LIMIT 1"), {"t": ticker}).fetchone()
            price = float(price_row[0]) if price_row else 100.0

            # Calculate cost with slippage and fees
            direction = 1 if action == "buy" else -1
            trade_cost = price * quantity * (1 + slippage_pct/100 + fees_pct/100) if direction == 1 else price * quantity

            # Enforce max allocation
            max_alloc_value = cash_available * (max_alloc_pct / 100.0)
            if direction == 1 and trade_cost > max_alloc_value:
                trade_cost = max_alloc_value
                quantity = max(trade_cost / price, 0)

            # Update cash and positions (simplified)
            if direction == 1:
                new_cash = max(cash_available - trade_cost, 0)
                db.execute(text("UPDATE portfolio SET cash_available=:c"), {"c": new_cash})
                db.execute(text("INSERT INTO positions (ticker, quantity) VALUES (:t, :q) ON CONFLICT (ticker) DO UPDATE SET quantity = positions.quantity + EXCLUDED.quantity"), {"t": ticker, "q": quantity})
            else:
                proceeds = price * quantity * (1 - fees_pct/100)
                new_cash = cash_available + proceeds
                db.execute(text("UPDATE portfolio SET cash_available=:c"), {"c": new_cash})
                db.execute(text("UPDATE positions SET quantity = GREATEST(positions.quantity - :q, 0) WHERE ticker=:t"), {"t": ticker, "q": quantity})

            # Log trade
            db.execute(text("INSERT INTO trades (ticker, action, quantity, price) VALUES (:t, :a, :q, :p)"), {"t": ticker, "a": action, "q": quantity, "p": price})
            db.commit()

            logger.info({"event": "trade_executed", "ticker": ticker, "action": action, "qty": quantity, "price": price})
            return {"ticker": ticker, "action": action, "quantity": quantity, "price": price, "cash_available": new_cash}