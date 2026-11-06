# KanekiGram (от ripx4)

## Файлы проекта
- server.py — сервер (Flask)
- index.html — интерфейс приложения
- style.css — стиль (Tokyo Ghoul: тёмная тема, красные акценты)
- requirements.txt — зависимости для Render
- users.json / messages.json — создаются автоматически при первом запуске

## Запуск на своём ПК (проверка)
    pip install flask
    python server.py
    Открой в браузере: http://localhost:8000

## Главный админ
Первый вход с ником ripx4 создаёт админ-аккаунт:
- бейдж ADMIN
- бесконечный баланс звёзд (∞)

## Остальные пользователи
- Регистрация через вкладку «Создать аккаунт»
- Старт: 100 звёзд, +5 звёзд каждый день при входе

## Деплой на Render (шаги)
1. Залить файлы на GitHub (git init / add / commit / push).
2. render.com → New + → Web Service → выбрать репозиторий.
3. Build Command: оставить пустым.
4. Start Command: python server.py
5. Создать сервис — получить постоянную ссылку вида https://kanekigram.onrender.com
