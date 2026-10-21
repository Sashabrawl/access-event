# AccessEvent — инклюзивная платформа мероприятий
 
Веб-платформа для организации мероприятий, доступная людям с
нарушениями слуха: визуальные уведомления вместо звуковых,
текстовый чат, цветовая индикация статусов.
 
## Стек технологий
 
| Слой | Технология |
|---|---|
| Backend | Python 3.11, Flask |
| База данных | PostgreSQL 16 |
| Frontend | HTML5, CSS3, JavaScript, Jinja2 |
| Тестирование | pytest |
| CI/CD | GitHub Actions |
| Контейнеризация | Docker, docker compose, GHCR |
 
## Как запустить
 
### Вариант 1. Docker (рекомендуется)
```
docker compose up
```
Открыть: http://127.0.0.1:5000
 
### Вариант 2. Локально
1. Скопировать .env.example в .env и заполнить:
   - SECRET_KEY=<случайная строка>
   - DATABASE_URL=postgresql://postgres:<пароль>@localhost:5432/accessevent
2. Установить зависимости: pip install -r requirements.txt
3. Запустить: python app.py
 
## Тесты
 
```
python -m pytest -v
```
 
## Структура проекта
 
access-event/
├── app.py                # точка входа, маршруты
├── models.py             # SQLAlchemy-модели
├── auth.py               # JWT, хеширование, роли
├── templates/            # Jinja2-шаблоны
├── static/css, static/js # стили и скрипты
├── tests/                # тесты pytest
├── docs/                 # вся документация
├── Dockerfile
└── docker-compose.yml
 
## Скриншоты
 
![Главная страница](docs/screenshots/01_main.png)
![Список мероприятий](docs/screenshots/03_create_event.png)
![Чат и уведомления](docs/screenshots/06_chat.png)
 
## Документация
 
- docs/analysis.md — анализ предметной области
- docs/requirements.md — требования и User Stories
- docs/stakeholders.md — стейкхолдеры
- docs/tz.md — техническое задание
- docs/architecture.md — архитектура системы
- docs/schema.sql — схема базы данных
- docs/er_diagram.png — ER-диаграмма
- docs/security.md — подсистема безопасности
- docs/test_cases.md — тест-кейсы
- docs/bug_reports.md — баг-репорты
- docs/user_manual.md — руководство пользователя
- docs/admin_manual.md — руководство администратора
- docs/api.md — описание API
- docs/assessment.md — оценка ИС и направления развития
- docs/presentation.pptx — презентация проекта
 
## Docker-образ
 
Образ публикуется автоматически при push (GitHub Actions):
 
```
ghcr.io/<ВАШ_ЛОГИН>/accessevent:latest
```
 
## Автор
 
<ФИО>, группа <X>, учебная практика ПМ.05, 3 семестр.
