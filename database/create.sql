/*
mysql -u root -p < create.sql

TODO: create a user to own this database
*/

/* drop the database if it exists */
drop database if exists chattest;

/* create the database */
create database chattest;

/* use the database */
use chattest;

/* create the accounts table */
create table accounts
(
    id integer not null auto_increment primary key,
    username varchar(64) not null unique,
    passwordmd5 char(32) not null,
    loggedin char(1) not null default 'N',
    can_login char(1) not null default 'N',
    valid char(1) not null default 'N',
    administrator char(1) not null default 'N'
);

/* add an administrator */
insert into accounts (username, passwordmd5, valid, administrator) values ('administrator', '200ceb26807d6bf99fd6f4f0d1ca54d4', 'Y', 'Y');

/* add test users */
insert into accounts (username, passwordmd5, can_login, valid) values ('test1', '098f6bcd4621d373cade4e832627b4f6', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('test2', '098f6bcd4621d373cade4e832627b4f6', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('test3', '098f6bcd4621d373cade4e832627b4f6', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('test4', '098f6bcd4621d373cade4e832627b4f6', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('test5', '098f6bcd4621d373cade4e832627b4f6', 'Y', 'Y');

/* add load test users */
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest1', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest2', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest3', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest4', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest5', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest6', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest7', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest8', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest9', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest10', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest11', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest12', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest13', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest14', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest15', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest16', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest17', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest18', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest19', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest20', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest21', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest22', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest23', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest24', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
insert into accounts (username, passwordmd5, can_login, valid) values ('loadtest25', '03a927e3728b7d3f910103d21f3bf74c', 'Y', 'Y');
