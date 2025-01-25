# test_betting-platform

## Structure
```
project-root/
├── docker-compose.yml  # Для управления сервисами (RabbitMQ, Redis, Celery, FastAPI, PostgreSQL)
├── .env                # Общие переменные окружения для всего проекта
├── pyproject.toml      # Конфигурация Poetry (зависимости для всего проекта)
├── poetry.lock         # Зафиксированные зависимости
├── line-provider/      # Сервис line-provider
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # Точка входа для сервиса
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── events.py  # Маршруты для API
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py  # Настройки Celery
│   │   │   ├── tasks.py       # Фоновые задачи
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── events.py  # Pydantic модели для событий
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── event_manager.py  # Логика работы с событиями
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py  # Общие утилиты
│   ├── migrations/       # Миграции базы данных line-provider
│   │   ├── versions/     # Версии миграций
│   │   └── env.py        # Конфигурация Alembic
│   ├── Dockerfile        # Docker-образ для line-provider
├── bet-maker/           # Сервис bet-maker
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # Точка входа для сервиса
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── bets.py    # Маршруты для API ставок
│   │   ├── consumers/
│   │   │   ├── __init__.py
│   │   │   ├── events_consumer.py  # Логика прослушивания очереди
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── bets.py  # Pydantic модели для ставок
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── bet_manager.py  # Логика работы с ставками
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py  # Общие утилиты
│   ├── migrations/       # Миграции базы данных bet-maker
│   │   ├── versions/     # Версии миграций
│   │   └── env.py        # Конфигурация Alembic
│   ├── Dockerfile        # Docker-образ для bet-maker
├── shared/              # Общие ресурсы
│   ├── __init__.py
│   ├── schemas/         # Общие Pydantic схемы
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── bets.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── celery.py     # Общая конфигурация Celery
│   │   ├── database.py   # Конфигурация подключения к PostgreSQL
│   │   ├── rabbitmq.py   # Конфигурация подключения к RabbitMQ
│   │   ├── redis.py      # Конфигурация подключения к Redis
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py     # Логирование
├── tests/               # Тесты
│   ├── line-provider/
│   ├── bet-maker/
├── README.md            # Описание проекта
```