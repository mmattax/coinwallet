create database coin;
use coin;
create table user (
  id integer unsigned not null primary key auto_increment,
  email varchar(50) not null, 
  first_name varchar(50) not null,
  last_name varchar(50) not null,
  password varchar(60) not null,
  api_key varchar(50) NULL
);
