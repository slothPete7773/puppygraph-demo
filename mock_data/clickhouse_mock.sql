CREATE DATABASE IF NOT EXISTS modern;
USE modern;
CREATE TABLE modern.person (
  id String,
  name String,
  age Int32
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO modern.person (id, name, age)
VALUES ('v1', 'marko', 29),
  ('v2', 'vadas', 27),
  ('v4', 'josh', 32),
  ('v6', 'peter', 35);
CREATE TABLE modern.software (
  id String,
  name String,
  lang String
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO modern.software (id, name, lang)
VALUES ('v3', 'lop', 'java'),
  ('v5', 'ripple', 'java');
CREATE TABLE modern.created (
  id String,
  from_id String,
  to_id String,
  weight Float64
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO modern.created (id, from_id, to_id, weight)
VALUES ('e9', 'v1', 'v3', 0.4),
  ('e10', 'v4', 'v5', 1.0),
  ('e11', 'v4', 'v3', 0.4),
  ('e12', 'v6', 'v3', 0.2);
CREATE TABLE modern.knows (
  id String,
  from_id String,
  to_id String,
  weight Float64
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO modern.knows (id, from_id, to_id, weight)
VALUES ('e7', 'v1', 'v2', 0.5),
  ('e8', 'v1', 'v4', 1.0);