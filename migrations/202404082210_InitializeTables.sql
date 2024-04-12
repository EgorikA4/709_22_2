-- migrate:up

create extension if not exists "uuid-ossp";

drop table if exists owners, hcs, properties, owners_properties cascade;

create table owners(
	id uuid primary key default uuid_generate_v4(),
	first_name text,
	last_name text,
	passport int,
	unique (passport)
);

create table hcs(
	id uuid primary key default uuid_generate_v4(),
	name text,
	phone text,
	address text,
	capital float
);

create table properties(
	id uuid primary key default uuid_generate_v4(),
	address text,
	square float,
	price float,
	hcs_id uuid references hcs
);

create table owners_properties(
	owners_id uuid references owners,
	properties_id uuid references properties,
	primary key (owners_id, properties_id)
);

-- migrate:down
