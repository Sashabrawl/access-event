from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_accessevent'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accessevent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- МОДЕЛИ БАЗЫ ДАННЫХ ---
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), default="Москва")
    has_sign_language = db.Column(db.Boolean, default=True)
    is_inclusive = db.Column(db.Boolean, default=True)

# --- БАЗОВЫЙ HTML ШАБЛОН (МЕНЮ И ПОДВАЛ) ---
BASE_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccessEvent</title>
    <style>
        /* Базовые стили */
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        :root {
            --bg-color: #f8f9fa; --text-color: #333; --card-bg: #ffffff;
            --nav-bg: #1a73e8; --footer-bg: #ffffff; --border-color: #ddd;
        }
        
        /* Ночная тема */
        body.dark-theme {
            --bg-color: #121212; --text-color: #e0e0e0; --card-bg: #1e1e1e;
            --nav-bg: #0f4c81; --footer-bg: #1e1e1e; --border-color: #333;
        }
        
        body { background-color: var(--bg-color); color: var(--text-color); transition: background 0.3s, color 0.3s; }
        
        nav { background-color: var(--nav-bg); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; color: white; }
        nav .logo { font-size: 1.5rem; font-weight: bold; text-decoration: none; color: white; }
        nav .links { display: flex; gap: 1.5rem; align-items: center; }
        nav .links a { color: white; text-decoration: none; font-weight: 500; }
        nav .links a:hover { text-decoration: underline; }
        
        /* Кнопка темы */
        .theme-btn { background: none; border: 1px solid white; color: white; padding: 0.4rem 0.8rem; border-radius: 5px; cursor: pointer; font-size: 1rem; }
        .theme-btn:hover { background: rgba(255,255,255,0.1); }
        
        .container { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
        
        footer { text-align: center; padding: 2rem; background: var(--footer-bg); color: #888; border-top: 1px solid var(--border-color); margin-top: 4rem; }
        
        .btn-primary { background: #1a73e8; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-primary:hover { background: #1557b0; }
        
        .alert { padding: 1rem; border-radius: 5px; margin-bottom: 1rem; background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        
        /* Карточки */
        .card { background: var(--card-bg); padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">⚡ AccessEvent</a>
        <div class="links">
            <a href="/">Главная</a>
            <a href="/events">Мероприятия</a>
            <a href="/login">Вход</a>
            <a href="/register">Регистрация</a>
            <button class="theme-btn" onclick="toggleTheme()">🌙 Тема</button>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>

    <footer>
        <p>AccessEvent — платформа инклюзивных мероприятий</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Визуальные уведомления вместо звуковых — для всех пользователей</p>
    </footer>

    <script>
        // Скрипт переключения темы
        function toggleTheme() {
            document.body.classList.toggle('dark-theme');
            // Запоминаем выбор пользователя
            if (document.body.classList.contains('dark-theme')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.setItem('theme', 'light');
            }
        }
        // При загрузке проверяем, не включал ли пользователь тему ранее
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-theme');
        }
    </script>
</body>
</html>
"""

# --- HTML СТРАНИЦЫ ---
INDEX_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
    <div style="background: linear-gradient(135deg, #e8f0fe, #d2e3fc); padding: 4rem 2rem; border-radius: 12px; text-align: center; margin-bottom: 2rem; color: #333;">
        <h1 style="font-size: 2.5rem; color: #1a73e8; margin-bottom: 1rem;">Платформа инклюзивных мероприятий</h1>
        <p style="font-size: 1.2rem; color: #555; margin-bottom: 2rem;">Находите события с сурдопереводом, визуальными оповещениями и доступной средой.</p>
        <a href="/events" class="btn-primary">Смотреть мероприятия</a>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
        <div class="card" style="text-align: center;">
            <h3>🔔 Уведомления</h3><p>Все уведомления визуальные.</p>
        </div>
        <div class="card" style="text-align: center;">
            <h3>👐 Сурдоперевод</h3><p>События с жестовым переводом помечены.</p>
        </div>
        <div class="card" style="text-align: center;">
            <h3>♿ Доступность</h3><p>Указаны условия доступности.</p>
        </div>
    </div>
""")

EVENTS_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
    <h1 style="margin-bottom: 1.5rem;">Мероприятия</h1>
    <a href="/add_event" class="btn-primary" style="margin-bottom: 2rem;">+ Создать мероприятие</a>
    
    <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
        <button class="btn-primary" style="background: #e8f0fe; color: #1a73e8;">Все</button>
        <button class="btn-primary" style="background: #e8f0fe; color: #1a73e8;">Только инклюзивные</button>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
        {% for event in events %}
        <div class="card">
            <h3 style="margin-bottom: 0.5rem;">{{ event.title }}</h3>
            <p style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">📅 {{ event.date }} • 📍 {{ event.location }}</p>
            <p style="margin-bottom: 1rem;">{{ event.description }}</p>
            <div>
                {% if event.is_inclusive %}<span style="background: #e6f4ea; color: #137333; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; margin-right: 5px;">Инклюзивное</span>{% endif %}
                {% if event.has_sign_language %}<span style="background: #e8f0fe; color: #1a73e8; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">Сурдоперевод</span>{% endif %}
            </div>
        </div>
        {% else %}
        <p>Пока нет мероприятий. Создайте первое!</p>
        {% endfor %}
    </div>
""")

ADD_EVENT_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
    <div class="card" style="max-width: 500px; margin: 0 auto;">
        <h2>Создать мероприятие</h2>
        <form method="POST" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
            <input type="text" name="title" placeholder="Название" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <input type="text" name="date" placeholder="Дата и время" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <input type="text" name="location" placeholder="Место" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <textarea name="description" placeholder="Описание" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color); resize: vertical;"></textarea>
            <button type="submit" class="btn-primary">Опубликовать</button>
        </form>
    </div>
""")

LOGIN_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
    <div class="card" style="max-width: 400px; margin: 0 auto;">
        <h2>Вход</h2>
        <form method="POST" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
            <input type="email" name="email" placeholder="Email" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <input type="password" name="password" placeholder="Пароль" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <button type="submit" class="btn-primary">Войти</button>
        </form>
        <p style="text-align: center; margin-top: 1rem;"><a href="/register" style="color: #1a73e8;">Нет аккаунта? Зарегистрируйтесь</a></p>
    </div>
""")

REGISTER_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
    <div class="card" style="max-width: 400px; margin: 0 auto;">
        <h2>Регистрация</h2>
        <form method="POST" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
            <input type="text" name="username" placeholder="Имя пользователя" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <input type="email" name="email" placeholder="Email" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <input type="password" name="password" placeholder="Пароль" required style="padding: 10px; border: 1px solid var(--border-color); border-radius: 5px; background: var(--bg-color); color: var(--text-color);">
            <label style="display: flex; align-items: center; gap: 0.5rem;">
                <input type="checkbox" name="is_deaf"> Я глухой или слабослышащий
            </label>
            <button type="submit" class="btn-primary">Зарегистрироваться</button>
        </form>
    </div>
""")

# --- МАРШРУТЫ ---
@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/events")
def events():
    all_events = Event.query.order_by(Event.id.desc()).all()
    if not all_events:
        e1 = Event(title="Инклюзивный концерт", description="Концерт с сурдопереводом", date="2026-12-01 18:00", location="Москва, КЗ")
        e2 = Event(title="IT-хакатон", description="Хакатон для всех", date="2026-11-15 10:00", location="Санкт-Петербург")
        db.session.add_all([e1, e2])
        db.session.commit()
        all_events = Event.query.all()
    return render_template_string(EVENTS_HTML, events=all_events)

@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        if title and description and date:
            new_e = Event(title=title, description=description, date=date, location=location)
            db.session.add(new_e)
            db.session.commit()
            flash("Мероприятие успешно создано!")
            return redirect(url_for('events'))
    return render_template_string(ADD_EVENT_HTML)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Вход выполнен успешно (демо-режим)!")
        return redirect(url_for('index'))
    return render_template_string(LOGIN_HTML)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash("Вы успешно зарегистрированы (демо-режим)!")
        return redirect(url_for('login'))
    return render_template_string(REGISTER_HTML)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)