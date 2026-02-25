CREATE TABLE redirect_stats_new (
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
ORDER BY (event_date, short_code);

INSERT INTO redirect_stats_new SELECT * FROM redirect_stats;

EXCHANGE TABLES redirect_stats AND redirect_stats_new;

DROP TABLE redirect_stats_new;
