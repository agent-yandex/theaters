-- migrate:up

insert into theaters.theater(title, address, rating)
select md5(random()::text), md5(random()::text), random() * 5
from generate_series(1, 100000);

-- migrate:down