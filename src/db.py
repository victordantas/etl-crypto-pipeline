from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Dict

def make_engine(conf: Dict) -> Engine:
    url = f"postgresql+psycopg2://{conf['user']}:{conf['password']}@{conf['host']}:{conf['port']}/{conf['name']}"
    engine = create_engine(url, pool_pre_ping=True)
    return engine

def upsert_dim_asset(engine: Engine, asset_id: str, symbol: str, name: str) -> None:
    sql = text("""
        INSERT INTO dim_asset (asset_id, symbol, name)
        VALUES (:asset_id, :symbol, :name)
        ON CONFLICT (asset_id) DO UPDATE SET symbol = EXCLUDED.symbol, name = EXCLUDED.name;
    """)
    with engine.begin() as conn:
        conn.execute(sql, {"asset_id": asset_id, "symbol": symbol, "name": name})

def insert_raw(engine: Engine, payload) -> None:
    sql = text("""INSERT INTO raw_crypto_prices (payload) VALUES (:payload::jsonb)""")
    with engine.begin() as conn:
        conn.execute(sql, {"payload": payload})

def upsert_fact_price(engine: Engine, rows: list[dict]) -> int:
    if not rows:
        return 0
    sql = text("""
        INSERT INTO fact_market_price
        (asset_id, symbol, price_usd, market_cap, last_updated, fetched_at)
        VALUES
        (:asset_id, :symbol, :price_usd, :market_cap, :last_updated, NOW())
        ON CONFLICT (asset_id, last_updated) DO UPDATE
        SET price_usd = EXCLUDED.price_usd,
            market_cap = EXCLUDED.market_cap;
    """)
    with engine.begin() as conn:
        res = conn.execute(sql, rows)
        return res.rowcount or 0