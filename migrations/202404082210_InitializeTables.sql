-- migrate:up

create extension if not exists "uuid-ossp";

create schema api_data;

create table api_data.owners(
	id uuid primary key default uuid_generate_v4(),
	first_name text,
	last_name text,
	passport int,
	unique (passport)
);

create table api_data.hcs(
	id uuid primary key default uuid_generate_v4(),
	name text,
	phone text,
	address text,
	capital float
);

create table api_data.properties(
	id uuid primary key default uuid_generate_v4(),
	address text,
	square float,
	price float,
	hcs_id uuid references api_data.hcs
);

create table api_data.owners_properties(
	owners_id uuid references api_data.owners,
	properties_id uuid references api_data.properties,
	primary key (owners_id, properties_id)
);

-- migrate:down
