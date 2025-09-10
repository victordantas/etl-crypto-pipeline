-- Raw ingestion (keep JSON for auditing/replays)
CREATE TABLE IF NOT EXISTS raw_crypto_prices (
  id SERIAL PRIMARY KEY,
  source TEXT NOT NULL DEFAULT 'coingecko',
  payload JSONB NOT NULL,
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Reference assets
CREATE TABLE IF NOT EXISTS dim_asset (
  asset_id TEXT PRIMARY KEY,          -- coingecko 'id' (e.g., 'bitcoin')
  symbol TEXT NOT NULL,
  name   TEXT NOT NULL
);

-- Fact table for market data snapshots
CREATE TABLE IF NOT EXISTS fact_market_price (
  asset_id TEXT NOT NULL REFERENCES dim_asset(asset_id),
  symbol   TEXT NOT NULL,
  price_usd NUMERIC(18,8) NOT NULL,
  market_cap BIGINT,
  last_updated TIMESTAMPTZ NOT NULL,
  fetched_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (asset_id, last_updated) -- prevents duplicates on re-runs
);