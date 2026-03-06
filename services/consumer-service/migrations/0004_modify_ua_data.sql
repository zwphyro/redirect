ALTER TABLE redirect_stats 
  MODIFY COLUMN browser Nullable(String),
  MODIFY COLUMN browser_version Nullable(String),
  MODIFY COLUMN os Nullable(String),
  MODIFY COLUMN os_version Nullable(String),
  MODIFY COLUMN device Nullable(String),
  MODIFY COLUMN device_brand Nullable(String),
  MODIFY COLUMN device_model Nullable(String),
  MODIFY COLUMN language Nullable(String),
  MODIFY COLUMN origin Nullable(String);
