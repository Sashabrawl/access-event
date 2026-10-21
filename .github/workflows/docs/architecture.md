# Архитектура системы AccessEvent

## 1. Трёхслойная архитектура

### Клиентский слой (Frontend)
- Технологии: HTML5, CSS3, JavaScript, Jinja2
- Компоненты: страницы событий, профиль, чат, визуальные уведомления
- Адаптация для глухих пользователей: цветовая индикация вместо звука

### Серверный слой (Backend)
- Технологии: Python 3.11+, Flask, SQLAlchemy
- Компоненты: маршрутизация, бизнес-логика, ORM, подсистема безопасности
- Паттерн: MVC (Model-View-Controller)

### Слой данных
- СУБД: PostgreSQL 15
- Таблицы: users, events, registrations, messages, event_categories,
  event_category_link, notifications

## 2. Клиент-серверное взаимодействие
- GET /events — список мероприятий
- POST /events — создание мероприятия
- PUT /events/{id} — обновление
- DELETE /events/{id} — удаление

## 3. Инфраструктура
- GitHub Actions — автоматизированная проверка (CI/CD)
- Docker — контейнеризация
- GHCR — реестр Docker-образов

