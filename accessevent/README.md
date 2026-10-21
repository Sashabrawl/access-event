# AccessEvent — День 4 (Frontend + Docker)

Файлы этого архива копируются в корень вашего проекта accessevent
(рядом с config.py, models.py, routes/, requirements.txt из Дня 3).

Структура:
- templates/ — base, index, events, login, register, profile
- static/css/style.css, static/js/main.js
- app.py — полный обновлённый файл с 5 маршрутами страниц (заменяет app.py из Дня 3)
- Dockerfile, .dockerignore, docker-compose.yml
- .github/workflows/docker-publish.yml, day4-check.yml

Запуск: docker compose up --build  ->  http://localhost:5000
Коммит: git add . && git commit -m "Day 4" && git push origin main
