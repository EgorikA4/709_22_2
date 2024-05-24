-- migrate:up

create index properties_price_square_idx on api_data.properties using btree(price, square);

create extension if not exists pg_trgm;
create index properties_address_trgm_idx on api_data.properties using gist(address gist_trgm_ops);

-- migrate:down
