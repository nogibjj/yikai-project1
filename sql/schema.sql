PRAGMA foreign_keys = ON;

CREATE TABLE users(
	username VARCHAR(20) NOT NULL PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
  numnews INTEGER DEFAULT 0,
  groupbysource INTEGER DEFAULT 0
);

CREATE TABLE sources(
  sourcename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL REFERENCES USERS(username),
  active INTEGER NOT NULL,
  PRIMARY KEY(sourcename,owner)
);

CREATE TABLE companies(
  companyname VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL REFERENCES USERS(username),
  active INTEGER NOT NULL,
  PRIMARY KEY(companyname,owner)
);