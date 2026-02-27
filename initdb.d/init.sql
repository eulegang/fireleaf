create type Stats as (
  hp int,
  atk int,
  def int,
  spa int,
  spd int,
  sp int
);

create type Attr as enum (
  'HP',
  'Attack',
  'Defense',
  'Special Attack',
  'Special Defense',
  'Speed'
);

create type growth as enum (
  'Fast',
  'Slow',
  'Medium Slow',
  'Medium Fast'
);

create type move_category as enum (
  'Physical',
  'Special',
  'Status'
);

create table ev (
  id serial primary key,
  amount int not null,
  attribute attr not null
);

create table types(
  id serial primary key,
  name varchar(16)
);

create table pokemon(
  id serial primary key,
  name varchar not null,
  primary_type serial references types(id) not null,
  secondary_type serial references types(id),
  growth growth not null,
  stats stats not null
);

create table moves(
  id serial primary key,
  name varchar(32) not null,
  ty serial references types(id) not null,
  power int not null,
  accuracy int not null
);

create table pokemon_ev(
  pokemon_id serial references pokemon(id) not null,
  ev_id serial references ev(id) not null
);

create table pokemon_moves(
  pokemon_id serial references pokemon(id) not null,
  move_id serial references moves(id) not null,
  level int,
  tm int
);

insert into types (name) values
  ('Normal'), ('Fire'), ('Water'), ('Electric'),
  ('Grass'), ('Ice'), ('Fighting'), ('Poison'),
  ('Ground'), ('Flying'), ('Psychic'), ('Bug'),
  ('Rock'), ('Ghost'), ('Dragon'), ('Dark'),
  ('Steel'), ('Fairy');
