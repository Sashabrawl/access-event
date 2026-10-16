# Руководство администратора AccessEvent

## 1. Системные требования
- Python 3.11+
- PostgreSQL 15+
- Docker 24+ (для контейнерного запуска)

## 2. Развёртывание
Локально:
  1. python -m venv venv, затем активируйте окружение
     (Windows: venv\Scripts\activate, macOS/Linux: source venv/bin/activate)
  2. pip install -r requirements.txt
  3. Настройте .env (см. раздел 3)
  4. python app.py

Контейнерно:
  docker compose up -d   # поднимет web и db
  docker compose down    # остановит

## 3. Переменные окружения (.env)
| Переменная | Назначение | Пример |
| DATABASE_URL | Подключение к PostgreSQL | postgresql://postgres:пароль@localhost:5432/accessevent |
| SECRET_KEY | Ключ подписи JWT | произвольная длинная строка |
| TESTING | Переключение на тестовую SQLite (только для тестов) | 1 |

## 4. Роли и права
| Роль | Права |
| guest | просмотр мероприятий |
| user | регистрация на мероприятия, чат, отзывы |
| organizer | всё user + создание/редактирование мероприятий |
| admin | всё organizer + модерация и блокировка |

## 5. Резервное копирование
  pg_dump -U postgres accessevent > backup_2026-11-01.sql
  Восстановление: psql -U postgres accessevent < backup_2026-11-01.sql

## 6. Типовые проблемы и решения
1. Password authentication failed — неверный пароль в .env.
2. Connection refused — не запущен сервис PostgreSQL.
3. Address already in use (порт 5000) — старый процесс не завершён.
4. Таблицы не создаются — проверьте, что app.py вызывает db.create_all().
5. Контейнер web падает сразу после старта — неверный DATABASE_URL внутри
   docker-compose.yml (должен указывать на хост db, а не localhost).

Создайте файл docs/api.md. Готовый шаблон с таблицей эндпоинтов из Дня 3 и примерами JSON:
# Описание API AccessEvent

| Метод | URL | Доступ | Вход (JSON) | Ответы |
| POST | /api/register | все | username, email, password, role | 201 user_id; 400 ошибки валидации |
| POST | /api/login | все | email, password | 200 token; 401 неверные данные |
| GET | /api/events | все | — | 200 список мероприятий |
| POST | /api/events | organizer | title, event_date, is_inclusive | 201 event_id; 401 без токена |
| POST | /api/events/<id>/register | user | — | 201; 400 повторная; 404 нет события |
| GET | /api/my-registrations | user | — | 200 список регистраций |
| GET | /api/events/<id>/chat | участники | — | 200 список сообщений |
| POST | /api/events/<id>/chat | участники | text | 201 сообщение |
| POST | /api/events/<id>/reviews | user | rating, text | 201 отзыв |

## Примеры

### POST /api/register — запрос
{"username": "anna", "email": "anna@mail.ru", "password": "Passw0rd!", "role": "user"}
### Ответ 201
{"user_id": 1, "message": "Пользователь создан"}

### POST /api/login — запрос
{"email": "anna@mail.ru", "password": "Passw0rd!"}
### Ответ 200
{"token": "eyJhbGciOiJIUzI1NiIs...", "role": "user"}

### POST /api/events — запрос (с токеном организатора)
{"title": "Тихий кинопросмотр", "event_date": "2026-11-03 19:00:00", "is_inclusive": true}
### Ответ 201
{"event_id": 5, "message": "Мероприятие создано"}

