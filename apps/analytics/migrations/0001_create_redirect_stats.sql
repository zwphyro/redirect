CREATE TABLE IF NOT EXISTS redirect_stats (
  event_date Date,
  event_time DateTime,

  short_code String,

  ip String,
  continent_code String,
  country_code String,
  region_code String,
  city String,
  provider String,
  lat Float64,
  lon Float64,

  browser String,
  browser_version String,
  os String,
  os_version String,
  device String,
  device_brand String,
  device_model String,

  language String,

  origin String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (short_code, event_time);
