# MBlog

![Python](https://img.shields.io/badge/Python-3.13.3-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.4-092E20?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.17.1-A31F34?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white)

REST API для блог-платформы на **Django + Django REST Framework**: посты, комментарии, лайки и OAuth-логин через Google.

## Функциональность

- **OAuth авторизация**
- **Посты**: CRUD, редактирование/удаление только своих постов
- **Лайки**: ставить like на пост
- **Swagger**: тест API
- **Django admin**: Админская панель

## Как Запустить (WIP)

Для запуска нужна база данных PostgreSQL и переменные окружения `.env`.

1. установить пакеты: `pip install -r requirements.txt`
2. запустить `pgAdmin`
3. запустить сервер: `python manage.py runserver`
4. создать суперпользователя: `python manage.py createsuperuser`
5. провести миграции: `python manage.py makemigrations` `python manage.py migrate`
6. создать `OAuth Client` в `Google Cloud Console`
7. создать переменные окружения в `.env`: смотри [Переменные окружения](#Переменные-окружения)
8. запустить сервер через консоль `python manage.py runserver` или использовать task `Run Django Server`
9. Перейти на один из эндпоинтов: [Основные-endpoints](#Основные-endpoints)

## Переменные окружения

Пример `.env`:

```bash
DEBUG=1
SECRET_KEY=change-me

DATABASE_URL=postgresql://username:password@localhost:5432/my_project_db

# Google OAuth (create OAuth Client in Google Cloud Console)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

## Используемые библиотеки

- `django-allauth` — OAuth авторизация
- `psycopg2-binary` — драйвер PostgreSQL
- `python-dotenv` — работа с переменными окружения

## Основные endpoints

### Глобальные

Админ панель: `http://127.0.0.1:8000/admin/`
Swagger: `http://127.0.0.1:8000/swagger/`
Google OAuth: `http://127.0.0.1:8000/accounts/google/login/`
