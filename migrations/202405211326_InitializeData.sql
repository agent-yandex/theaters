-- migrate:up

create extension if not exists "uuid-ossp";

create schema theaters;

create table theaters.performance
(
    id uuid primary key default uuid_generate_v4(),
    title text,
    description text,
    date date
);

create table theaters.theater
(
    id uuid primary key default uuid_generate_v4(),
    title text,
    address text,
    rating float
);

create table theaters.theater_performance
(
    id uuid primary key default uuid_generate_v4(),
    theater_id uuid references theaters.theater,
    performance_id uuid references theaters.performance
);

create table theaters.ticket
(
    id uuid primary key default uuid_generate_v4(),
    time time,
    place text,
    theater_performance_id uuid references theaters.theater_performance
);

insert into theaters.theater(title, address, rating) values
('Большой', 'Анархии 12', 4.12),
('Малый', 'Ленина 32', 3.23),
('Средний', 'Просвещения 56', 4.8);

insert into theaters.performance(title, description, date) values
('Лебединое озеро', 'Первая постановка', '2024.12.12'),
('Щелкунчик', 'Вторая постановка', '2024.12.12'),
('Концерт молодых чтецов', 'Третья постановка', '2024.12.12');

insert into theaters.theater_performance(theater_id, performance_id) values
((select id from theaters.theater where title = 'Большой'),
 (select id from theaters.performance where title = 'Лебединое озеро')),
((select id from theaters.theater where title = 'Малый'),
 (select id from theaters.performance where title = 'Щелкунчик')),
((select id from theaters.theater where title = 'Средний'),
 (select id from theaters.performance where title = 'Концерт молодых чтецов'));

insert into theaters.ticket(time, place, theater_performance_id) values
('12:00', '12 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Лебединое озеро')),
('12:00', '13 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Лебединое озеро')),
('12:00', '14 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Лебединое озеро')),
('12:00', '12 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Щелкунчик')),
('12:00', '13 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Щелкунчик')),
('12:00', '14 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Щелкунчик')),
('12:00', '12 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Концерт молодых чтецов')),
('12:00', '13 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Концерт молодых чтецов')),
('12:00', '14 место',
 (select tp.id from theaters.theater_performance tp
  join theaters.performance p on p.id = tp.performance_id
  where title = 'Концерт молодых чтецов'));

-- migrate:down