-- migrate:up

create index theaters_rating_idx on theaters.theater using btree(rating);

create extension pg_trgm;

create index theaters_title_address_idx on theaters.theater using gist(title gist_trgm_ops, address gist_trgm_ops);

-- migrate:down