CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  text1 TEXT,
  text2 TEXT
);

COPY items(text1, text2) FROM '/docker-entrypoint-initdb.d/train_normalized_1.csv' DELIMITER '|' CSV HEADER;
COPY items(text1, text2) FROM '/docker-entrypoint-initdb.d/train_normalized_2.csv' DELIMITER '|' CSV HEADER;
