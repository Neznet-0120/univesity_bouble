# Frontend for University project

Простой, быстрый фронтенд на HTML + Vanilla JS для существующего Django REST API.

## Быстрый старт

1. Откройте терминал и перейдите в папку фронтенда:

```powershell
cd frontend
```

2. Запустите любой локальный сервер (Python, Node, Live Server и т.д.) на порт 8080 или другой:

```powershell
# Если у вас установлен Python:
python -m http.server 8080

# Или если у вас есть Node.js и установлен http-server:
npx http-server -p 8080
```

3. Откройте браузер и перейдите на `http://localhost:8080`

4. По умолчанию фронтенд обращается к бэкенду на `http://localhost:8000/api`. Если бэкенд на другом адресе, отредактируйте строку в `index.html`:

```javascript
const API_BASE = 'http://localhost:8000/api'; // Измените адрес здесь
```

## Возможности

- **Вход/Выход**: Использует Django Token Auth
- **Dashboard**: Показывает последние новости и ближайшие уроки
- **Новости**: Просмотр всех новостей
- **Расписание**: Просмотр всех уроков
- **Профиль**: Информация текущего пользователя

## API эндпоинты

Фронтенд использует следующие эндпоинты вашего бэкенда:
- `POST /api/auth/login/` — вход (username, password)
- `POST /api/auth/logout/` — выход
- `GET /api/news/` — список новостей
- `GET /api/lessons/` — расписание
- `GET /api/profiles/me/` — данные текущего пользователя

Все запросы автоматически включают заголовок `Authorization: Token <token>`