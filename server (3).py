import os
import json
from datetime import date
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

USERS_FILE = "users.json"
MESSAGES_FILE = "messages.json"

ADMIN_NICK = "ripx4"
START_STARS = 100
DAILY_BONUS = 5


def load(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


users = load(USERS_FILE, {})
messages = load(MESSAGES_FILE, [])


def user_stars(u):
    return "∞" if u["role"] == "admin" else u["stars"]


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify({"error": "Введите ник и пароль"}), 400
    if len(username) > 20:
        return jsonify({"error": "Ник слишком длинный (максимум 20)"}), 400
    if username in users:
        return jsonify({"error": "Такой ник уже занят"}), 400
    if username == ADMIN_NICK:
        users[username] = {"password": password, "stars": None, "role": "admin", "last_bonus": ""}
    else:
        users[username] = {"password": password, "stars": START_STARS, "role": "user", "last_bonus": ""}
    save(USERS_FILE, users)
    return jsonify({"ok": True, "message": "Аккаунт создан! Добро пожаловать в KanekiGram"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    u = users.get(username)
    if not u or u["password"] != password:
        return jsonify({"error": "Неверный ник или пароль"}), 400
    bonus_msg = None
    today = date.today().isoformat()
    if u["role"] != "admin" and u.get("last_bonus") != today:
        u["stars"] = u["stars"] + DAILY_BONUS
        u["last_bonus"] = today
        save(USERS_FILE, users)
        bonus_msg = "Ежедневный бонус: +5 звёзд"
    return jsonify({
        "ok": True,
        "username": username,
        "role": u["role"],
        "stars": user_stars(u),
        "bonus": bonus_msg,
    })


@app.route("/api/me", methods=["POST"])
def me():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    u = users.get(username)
    if not u:
        return jsonify({"error": "Пользователь не найден"}), 400
    return jsonify({"ok": True, "username": username, "role": u["role"], "stars": user_stars(u)})


@app.route("/api/messages", methods=["GET"])
def get_messages():
    try:
        since = int(request.args.get("since", 0))
    except ValueError:
        since = 0
    return jsonify({"ok": True, "messages": messages[since:]})


@app.route("/api/send", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    text = (data.get("text") or "").strip()
    u = users.get(username)
    if not u:
        return jsonify({"error": "Сначала войдите в аккаунт"}), 401
    if not text:
        return jsonify({"error": "Пустое сообщение"}), 400
    if len(text) > 500:
        text = text[:500]
    messages.append({
        "user": username,
        "role": u["role"],
        "text": text,
        "time": __import__("time").strftime("%H:%M"),
    })
    save(MESSAGES_FILE, messages)
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("KanekiGram запущен! Открой в браузере: http://localhost:" + str(port))
    app.run(host="0.0.0.0", port=port)
