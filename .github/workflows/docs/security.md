# Подсистема безопасности AccessEvent

## 1. Аутентификация

### Регистрация
- Пользователь указывает: username, email, password
- Пароль хешируется через Werkzeug (pbkdf2:sha256)
- Хранится только password_hash, пароль в открытом виде не сохраняется

### Вход (login)
- Пользователь вводит email и пароль
- Сервер проверяет хеш через check_password_hash()
- При успехе генерируется JWT-токен (access token, срок 1 час)
- Выдаётся refresh token (срок 30 дней)

### Проверка токена
- Каждый запрос: заголовок Authorization: Bearer <token>
- Сервер декодирует JWT, проверяет подпись и срок действия
- При истечении access token — обновление через refresh token

## 2. Хеширование паролей
- Метод: pbkdf2:sha256 (Werkzeug)
- Пример: generate_password_hash("pass123", method='pbkdf2:sha256')
- Проверка: check_password_hash(stored_hash, "pass123")

## 3. Авторизация (RBAC)

### Роли
| Роль | Права |
|------|-------|
| guest | Просмотр событий и категорий |
| user | Регистрация на события, чат, уведомления, профиль |
| organizer | Создание и управление событиями (все права user) |
| admin | Управление пользователями, модерация (все права organizer) |

### Наследование прав
guest -> user -> organizer -> admin

### Реализация
- Декоратор @role_required(*roles) проверяет роль из JWT
- При недостатке прав — HTTP 403 Forbidden

## 4. JWT (JSON Web Token)
- Header: {"alg": "HS256", "typ": "JWT"}
- Payload: {"user_id": 1, "role": "organizer", "exp": 1700000000}
- Signature: HMAC-SHA256 с секретным ключом приложения

## 5. Инклюзивные функции безопасности
- Поле is_deaf в таблице users — адаптация интерфейса
- Визуальные уведомления (таблица notifications) вместо звуковых
- Текстовый чат (таблица messages) вместо голосового общения
- Цветовая индикация статусов (pending=жёлтый, confirmed=зелёный, cancelled=красный)
