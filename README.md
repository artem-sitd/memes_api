# memes_api

Memes API - это RESTful API для управления мемами, созданный с использованием FastAPI, PostgreSQL, SQLAlchemy и MinIO для хранения изображений.

## Установка:

1. Клонирование репозитория

> git clone https://github.com/artem-sitd/memes_api.git

1.1 Редактирование переменных окружения:
необходимо переименовать файл `.env.docker.template` в `.env.docker` (**можете его не редактировать, но вот пояснения
для каждой переменной**)
> `POSTGRES_USER`- имя пользователя базы postgres, которую создаст докер контейнер \
`POSTGRES_PASSWORD` - пароль пользователя базы postgres, которую создаст докер контейнер \
`POSTGRES_HOST` - название контейнера postgres\
`POSTGRES_DB` - название базы, которую создаст контейнер postgres\
`test_db` - название тестовой базы, используется в pytest, вне контейнера\
`MINIO_ROOT_USER` - имя пользователя, создает контейнер с клиентом S3 minio\
`MINIO_ROOT_PASSWORD` - пароль для пользователя, создает контейнер с клиентом S3 minio\
`access_key` - ключ для S3 minio, указываем просто как minio\
`secret_key` - секретный ключ для S3 minio, указываем просто как minio\
`endpoint_url` - путь до контейнера с S3 minio\
`bucket_name` - можете указать другой либо оставить, но в п.3 необходимо создать с таким же именем\
`test_bucket_name` - название бакета при тестах в pytest, логика такая же как и в п.3\

2. Сборка и запуск докер контейнеров

> docker-compose up --build

3. После сборки и запуска всех контейнеров - необходимо создать бакет в S3 minio,
   для этого - переходим по адресу: `http://localhost:9001/buckets`, справа будет кнопка "Create Backet",
   даем название бакету - которая указана в вашем `.env.docker` в переменной `bucket_name`

4. Можно пользоваться приложением.

## Использование

API предоставляет следующие конечные точки:

- `POST /post_memes` - создание мема.
- `GET /get_memes/{id}` - получение мема по ID.
- `GET /get_memes` - получение списка всех мемов.
- `PUT /put_memes/{id}` - обновление мема.
- `DELETE /delete_memes/{id}` - удаление мема.

Документация API находится по адресу `localhost:8000/docs`

## Структура проекта

- `main.py` - основной файл приложения FastAPI.
- `public_api/models.py` - описание моделей SQLAlchemy.
- `public_api/schemas.py` - описание Pydantic схем.
- `public_api/crud.py` - функции для взаимодействия с базой данных.
- `media_api/s3connect.py` - класс для работы с S3 (функции для управления файлами в minio).
- `alembic/` - настройки для миграций базы данных.
- `tests/` - тесты Pytest.
- `settings.py` - настройки для подключения к postgres и S3 minio.
