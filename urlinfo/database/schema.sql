DROP TABLE IF EXISTS urlinfo;

CREATE TABLE urlinfo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT UNIQUE NOT NULL,
  malware INTEGER NOT NULL
);