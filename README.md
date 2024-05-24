# Тестовое веб-приложение на Flask, реализующее CRUD

## База данных

* Для `id` используется тип `uuid`
* В запросах к базе предусмотрена защита от SQL инъекций
* Схема и база отличные от стандартных
* Раскатка базы данных производится при помощи миграций
* CRUD реализован для таблицы `theater`
* Использование индексов для быстрого поиска
* Использование генерации случайных данных

<img width="795" alt="Снимок экрана 2024-05-21 в 18 41 03" src="https://github.com/agent-yandex/theaters/assets/88597840/cbe853a3-c26c-4a77-a858-a0ffd2493682">

## Запуск

`docker compose up` - стандартный запуск<br>
`docker compose up -d` - запуск в detach моде<br>
`docker compose up --build` - запуск с пребилдом<br>
`docker compose stop` - остановка<br>
`docker compose down` - остановка и удаление контейнеров<br>
`docker compose up postgres migrator -d` - запуск сервисов отдельно