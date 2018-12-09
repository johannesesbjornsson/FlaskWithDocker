CREATE DATABASE products;
use products;

CREATE TABLE api_keys(
  api_key VARCHAR(255) NOT NULL,
  product VARCHAR(255) NOT NULL,
  userid VARCHAR(255) NOT NULL,
  PRIMARY KEY (api_key)
);

INSERT INTO api_keys
  (api_key, product, userid)
VALUES
  ('123', 'api_keys','jesbjorn');

