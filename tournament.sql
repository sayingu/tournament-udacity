-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- delete database because to recreate the tables
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- players table
CREATE TABLE Players (
	id SERIAL primary key,
	name varchar(255)
);

-- matches table
CREATE TABLE Matches (
	id SERIAL primary key,
	winner int references Players(id),
	loser int references Players(id)
);