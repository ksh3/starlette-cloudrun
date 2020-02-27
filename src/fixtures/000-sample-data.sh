#!/bin/bash
psql -U docker -d docker << EOL
create database docker;
create table robots (id int PRIMARY KEY, name varchar, created_at timestamp);
insert into robots (id, name, created_at) values (1, 'GUIDO', '2020-01-01');
EOL
