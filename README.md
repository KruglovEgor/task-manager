# Task Manager API

Простое API для управления задачами, разработанное с использованием FastAPI.

## 🛠 Технологии

- **Backend**: FastAPI
- **База данных**: SQLite
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Тестирование**: pytest
- **Контейнеризация**: Docker + Docker Compose
- **Документация**: Swagger/OpenAPI

## 🚀 Быстрый старт

### 🐳 Docker (рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd task-manager
   ```

2. Запустите приложение:
   ```bash
   # Windows
   .\run.bat app

   # Linux/Mac
   .\run.sh app
   ```
   Приложение будет доступно по адресу:
   - API: http://localhost:8000
   - Swagger документация: http://localhost:8000/docs

3. Запустите тесты:
   ```bash
   # Windows
   .\run.bat test

   # Linux/Mac
   .\run.sh test
   ```

### ⚡ Локальный запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd task-manager
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # или
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Примените миграции:
   ```bash
   alembic upgrade head
   ```

4. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```
   Приложение будет доступно по адресу:
   - API: http://localhost:8000
   - Swagger документация: http://localhost:8000/docs

5. Запустите тесты:
   ```bash
   pytest
   ```

## 📋 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/` | Информация об API |
| GET | `/health` | Проверка состояния |
| GET | `/docs` | Swagger документация |
| POST | `/api/v1/tasks/` | Создать задачу |
| GET | `/api/v1/tasks/` | Получить список задач |
| GET | `/api/v1/tasks/{task_id}` | Получить задачу по ID |
| PUT | `/api/v1/tasks/{task_id}` | Обновить задачу |
| DELETE | `/api/v1/tasks/{task_id}` | Удалить задачу |

## 📊 Модель данных

### Task
- `id` (UUID) - уникальный идентификатор
- `title` (str) - название задачи
- `description` (str) - описание задачи
- `status` (enum) - статус: "создано", "в работе", "завершено"
- `created_at` (datetime) - дата создания
- `updated_at` (datetime) - дата обновления

## ⚙️ Конфигурация

Настройки приложения можно изменить в файле `.env`. Скопируйте `env.example` в `.env` и отредактируйте его.

```ini
# Application settings
APP_NAME=Task Manager
APP_VERSION=1.0.0
DEBUG=True

# Server settings
HOST=0.0.0.0
PORT=8000

# Database settings
DB_NAME=task_manager.db

# CORS settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```



## 🐳 Docker команды

```bash
# Запуск приложения
.\run.bat app

# Запуск тестов
.\run.bat test

# Остановка всех сервисов
.\run.bat stop

# Очистка контейнеров и образов
.\run.bat clean
```


