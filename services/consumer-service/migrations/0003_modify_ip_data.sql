ALTER TABLE redirect_stats 
  MODIFY COLUMN continent_code Nullable(String),
  MODIFY COLUMN country_code Nullable(String),
  MODIFY COLUMN region_code Nullable(String),
  MODIFY COLUMN city Nullable(String),
  MODIFY COLUMN provider Nullable(String),
  MODIFY COLUMN lat Nullable(Float64),
  MODIFY COLUMN lon Nullable(Float64);
