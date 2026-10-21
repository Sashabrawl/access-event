# Баг-репорты AccessEvent

## BUG-01. [Major] Повторная регистрация с тем же email возвращает 500
- Серьёзность: Major
- Приоритет: P2
- Шаги воспроизведения:
  1. POST /api/register с email test@mail.ru
  2. POST /api/register ещё раз с тем же email
- Фактический результат: 500 Internal Server Error
- Ожидаемый результат: 400 с понятным сообщением
- Статус: Исправлен

## BUG-02. [Major] Регистрация принимает email без @
- Серьёзность: Major
- Приоритет: P2
- Шаги воспроизведения:
  1. POST /api/register с email "not-an-email"
- Фактический результат: 201, пользователь создан
- Ожидаемый результат: 400, сообщение о неверном формате
- Статус: Исправлен

## BUG-03. [Minor] Бейдж статуса регистрации плохо читается в тёмной теме
- Серьёзность: Minor
- Приоритет: P3
- Шаги воспроизведения:
  1. Открыть /events в тёмной теме браузера
  2. Посмотреть бейдж статуса
- Фактический результат: жёлтый текст на светлом фоне почти не читается
- Ожидаемый результат: читаемость в обеих темах (проверка контрастности)
- Статус: Не исправлен + причина: правки стилей выходят за объём дня, перенесено в День 6

Шаг 3. Исправьте найденные ошибки в коде (отладка), перезапустите тесты и убедитесь, что они проходят. Для BUG-01 типовое исправление в routes/auth.py — проверка существования email до добавления в БД:
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if "@" not in email or "." not in email:
        return jsonify({"error": "Некорректный email"}), 400
    if len(password) < 8:
        return jsonify({"error": "Пароль: минимум 8 символов"}), 400

    if User.query.filter_by(email=email).first() is not None:
        # было: падение 500 из-за UNIQUE-конфликта (BUG-01)
        return jsonify({"error": "Email уже зарегистрирован"}), 400

    user = User(username=data.get("username"), email=email,
                password_hash=generate_password_hash(password),
                role=data.get("role", "user"))
    db.session.add(user)
    db.session.commit()
    return jsonify({"user_id": user.id}), 201
Сверьте код с вашим routes/auth.py из Дня 3 — если проверка уже есть, пометьте BUG-01 как Исправлен со ссылкой на неё.
