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
  name varchar(16) unique not null,
  category move_category not null
);

create table pokemon(
  id serial primary key,
  name varchar not null unique,
  primary_type integer references types(id) not null,
  secondary_type integer references types(id),
  growth growth not null,
  stats stats not null
);

create table moves(
  id serial primary key,
  name varchar(32) not null unique,
  ty integer references types(id) not null,
  power int,
  accuracy int
);

create table pokemon_ev(
  pokemon_id integer references pokemon(id) not null,
  ev_id integer references ev(id) not null
);

create table pokemon_moves(
  pokemon_id integer references pokemon(id) not null,
  move_id integer references moves(id) not null,
  level int,
  tm int
);

insert into types (name, category) values
  ('Normal', 'Physical'), ('Fire', 'Special'), ('Water', 'Special'), ('Electric', 'Special'),
  ('Grass', 'Special'), ('Ice', 'Special'), ('Fighting', 'Physical'), ('Poison', 'Physical'),
  ('Ground', 'Physical'), ('Flying', 'Physical'), ('Psychic', 'Special'), ('Bug', 'Physical'),
  ('Rock', 'Physical'), ('Ghost', 'Physical'), ('Dragon', 'Special'), ('Dark', 'Special'),
  ('Steel', 'Physical'), ('Fairy', 'Special'), ('???', 'Special');
