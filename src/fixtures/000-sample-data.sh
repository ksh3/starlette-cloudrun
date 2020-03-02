#!/bin/bash
psql -U docker -d docker << EOL
create database docker;
create table robots (id int PRIMARY KEY, name varchar, count bigint, created_at timestamp);
insert into robots (id, name, count, created_at) values (1, 'GUIDO', 0, '2020-01-01');
EOL
