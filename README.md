# MBlog

![Python](https://img.shields.io/badge/Python-3.13.3-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.4-092E20?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.17.1-A31F34?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker--2496ED?logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v2-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-latest-009639?logo=nginx&logoColor=white)

REST API для блог-платформы на **Django + Django REST Framework**: посты, лайки, Swagger/Redoc, OAuth-логин через Google.

## Функциональность

- **OAuth авторизация**
- **Посты**: CRUD, редактирование/удаление только своих постов (owner-only)
- **Лайки**: CRUD лайков через API
- **Фильтрация/сортировка постов**: фильтры по автору/дате и сортировка (см. Swagger)
- **Swagger/Redoc**: интерактивная документация API
- **Django admin**: админка

## Как Запустить

Ниже два варианта запуска:

- **Запуск вручную (локально)**: Python + PostgreSQL на твоей машине.
- **Запуск через Docker**: всё поднимается через `docker-compose` (PostgreSQL + Django/Gunicorn + Nginx).

### Способ 1. Запуск вручную (локально)

Для запуска нужна база данных PostgreSQL и переменная окружения `DATABASE_URL`.

1. Если ты хочешь изолировать зависимости проекта от системы и других проектов, то cоздай и активируй виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Подними PostgreSQL и создай базу через pgAdmin/psql. Подробности [здесь](https://github.com/Mark65537/MBlog/wiki/%D0%91%D0%B0%D0%B7%D0%B0-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85)
4. Создай файл `.env` в корне проекта (пример [Переменные окружения](#Переменные-окружения)).
5. Прогони миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Создай суперпользователя (для админки):

```bash
python manage.py createsuperuser
```

7. Запусти сервер:

```bash
python manage.py runserver
```

или используй task `Run Django Server`

8. Перейти на один из эндпоинтов: [Основные-endpoints](#Основные-endpoints)

### Способ 2. Запуск через Docker

Требуется установленный **Docker Desktop** (вместе с Docker Compose).

1. Создай файл `.env` в корне проекта (если ещё нет). Для запуска через `docker-compose` важно, чтобы хост БД был `db` (это имя сервиса в compose):

2. Собери и подними контейнеры:

```bash
docker compose up --build
```

или используй task `Run Docker`

3. Создать суперпользователя (Обычно нужно один раз):

```bash
docker compose exec web python manage.py createsuperuser
```

4. Перейти на один из эндпоинтов: [Основные-endpoints](#Основные-endpoints)

## Переменные окружения

Пример `.env`:

```bash
DEBUG=1
SECRET_KEY=change-me

# Обязательно. Формат:
# postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
DATABASE_URL=postgresql://postgres:password@localhost:5432/mblog_db
```

## Регистрация пользователя

пользователи могут зарегистрироваться только через Google аккаунт

### Настройка Google Application

сначала нужно создать `OAuth Client` в `Google Cloud Console`

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Зайдите под своим Google-аккаунтом. Если у вас нет двухфакторной аутентификации то нужно ее включить.
3. Создайте новый проект. Для этого нажмите на "название проекта" → New project. Задайте имя проекту, например `OAuth project`
4. Перейдите в `Navigation menu` или намите '.'
5. APIs & Servises → OAuth consent screen
6. Нажимите Get Started
7. Вводим имя и почту, например `oauthtest`, почту желательно ввести свою гугловскую
8. Далее Выберите External
9. В финише ставим галочку и create
10. потом Create OAuth client
11. выбираем webapplication.
12. в Authorized redirect URIs добавляем `http://127.0.0.1:8000/accounts/google/login/callback/`
13. Перейдите на `http://127.0.0.1:8000/admin/`
14. в разделе **Sites** добавить **Social application** (Google) в админке: client id / secret берутся из Google Cloud Console
15. Перейдите на `http://127.0.0.1:8000/accounts/google/login/`

## Основные endpoints

### Глобальные

Админ панель: `http://127.0.0.1:8000/admin/`
Swagger: `http://127.0.0.1:8000/swagger/`
Redoc: `http://127.0.0.1:8000/redoc/`
Google OAuth: `http://127.0.0.1:8000/accounts/google/login/`

### API

Базовый префикс: `/api/`

- Посты: `http://127.0.0.1:8000/api/posts/`
- Лайки: `http://127.0.0.1:8000/api/likes/`

Подсказка: поддерживаемые фильтры/сортировка и примеры запросов удобнее всего смотреть в Swagger (`/swagger/`).
