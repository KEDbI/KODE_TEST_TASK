Тестовое задание для KODE Education

В проекте реализован сервис, предоставляющий REST API интерфейс с методами: добавление заметок, вывод списка заметок. Также реализована базовая аутентификация и авторизация. 

Используется база данных Postgres. Скрипты для создания таблиц следующие:
1. Таблица users:
   CREATE TABLE users (id BIGSERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE, password VARCHAR(255))
2. Таблица notes:
   CREATE TABLE notes (id BIGSERIAL PRIMARY KEY, user_id INT REFERENCES users(id), note VARCHAR(255))

По заданию требовалось упаковать проект в Docker контейнер, но я с этим пока не разобрался. 
