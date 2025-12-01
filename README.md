# University Double — платформа для университета

Ниже — подробная документация по структуре проекта и по основным файлам. Документ написан так, чтобы разработчик, открывший репозиторий, мог быстро понять назначение каждого важного файла/модуля.

**Коротко:** Django-проект для хранения расписания, новостей и управления пользователями (студенты, преподаватели, админы факультетов). Есть простое REST API и экспорт расписания (iCal / PDF / Excel).

---

## Как запустить (кратко)
- Создать виртуальное окружение и активировать (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Установить зависимости (рекомендуется создать `requirements.txt` и затем `pip install -r requirements.txt`):

```powershell
pip install --upgrade pip
pip install django djangorestframework xhtml2pdf openpyxl icalendar
```

- Миграции и супер-пользователь:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

- Запуск dev-сервера:

```powershell
python manage.py runserver
```

Admin: `http://127.0.0.1:8000/admin/` — публичная часть: `/`.

---

## Файловая справка — важные файлы и что в них делает
Ниже перечислены ключевые файлы и папки с коротким пояснением их назначения и важными функциями.

- `manage.py` — стандартная точка входа Django для выполнения команд (`runserver`, `migrate`, `createsuperuser`).

- `db.sqlite3` — файл SQLite (используется для разработки). Для продакшена рекомендуется заменить на PostgreSQL.

### `university/` (проект)
- `university/asgi.py` — точка входа ASGI для асинхронного сервера (если используете Daphne/Uvicorn).
- `university/wsgi.py` — WSGI-приложение для Gunicorn/uWSGI.
- `university/urls/main.py` — главный роутер приложения: регистрирует `admin/`, `accounts/` и маршруты API (`api/` через DRF router). Здесь подключены представления `home` и `faculty_detail`.

#### `university/settings/`
- `base.py` — базовые (общие) настройки проекта: INSTALLED_APPS (включая `rest_framework`), middleware, шаблоны, статические файлы, `AUTH_USER_MODEL = 'core.User'`, локаль (`ru-ru`) и пр.
- `development.py` — настройки для разработки: `DEBUG = True`, `ALLOWED_HOSTS` и SQLite DB (используется при локальной разработке).
- `production.py` — файл существует (пустой сейчас) — сюда поместите настройки продакшна (секреты, DB, allowed hosts).

### `accounts/` (регистрация, вход, личный кабинет)
- `accounts/views.py` — ключевые представления:
	- `register` — форма регистрации (использует `RegistrationForm` из `forms.py`).
	- `user_login` / `user_logout` — обработка аутентификации.
	- `home` / `faculty_detail` — представления, которые используются в корневых маршрутах проекта.
	- `cabinet` — личный кабинет пользователя: показывает расписание для текущего пользователя (студент/преподаватель/админ факультета).
	- `export_ical` — экспорт расписания в формат `.ics` (использует `icalendar`).
	- `export_pdf` — экспорт расписания в PDF (использует `xhtml2pdf` и шаблон `schedule/pdf_raspisanie.html`).
	- `export_excel` — экспорт в Excel (`openpyxl`).
- `accounts/urls.py` — маршруты для регистрации, логина, кабинета и экспортов (`export/ical/`, `export/pdf/`, `export/excel/`).
- `accounts/forms.py` — `RegistrationForm` расширяет `UserCreationForm` и добавляет выбор роли (student/teacher), валидацию и автоматическое заполнение факультета/группы.
- `accounts/models.py` — в текущей версии пустой (логика пользователя находится в `core.User`).
- `accounts/admin.py` — регистрация моделей в админке (пока пустая или минимальная).

### `core/` (основные модели и утилиты)
- `core/models.py` — содержит основные модели: `Faculty`, `Department`, `Classroom`, и кастомную модель пользователя `User` (наследует `AbstractUser`), с полями `role`, `faculty`, `department`, `status`, `phone`, `photo`, `group`.
	- `User` используется как `AUTH_USER_MODEL`.
- `core/views.py` — пустой/заглушка для дополнительных общих представлений.
- `core/admin.py` — содержит вспомогательные админ-классы (например фильтр по факультету) — используется в других `admin.py`.

### `groups_app/` (группы студентов)
- `groups_app/models.py` — `StudentGroup` модель: `name`, `faculty`, `course`, `students` (ManyToMany к `core.User`). Полезные методы: `students_count()`.
- `groups_app/views.py` / `tests.py` / `admin.py` — вспомогательные, `admin.py` регистрирует модели в админке.

### `schedule/` (расписание)
- `schedule/models.py` — модель `Lesson` с полями: `subject`, `teacher (FK core.User)`, `group (FK StudentGroup)`, `classroom`, `day`, `time_start`, `time_end`, `week_type`. Порядок сортировки по дню и времени.
- `schedule/admin.py` — `LessonAdmin` с фильтрами, поиском и `autocomplete_fields`.
- `schedule/views.py` и `schedule/urls.py` — в репозитории пустые/заглушки; основная часть экспорта расписания реализована в `accounts.views` (экспорт iCal/PDF/Excel) и в модели `Lesson`.

### `news/` (новости)
- `news/models.py` — модель `News` с `title`, `content`, `faculty` (опционально), `created_at`, `updated_at`, `is_published`, `image`.
- `news/views.py` / `news/admin.py` — представления и админ-интеграция для управления новостями (используются в `accounts.home` и `faculty_detail`).

### `api/` (REST API)

В репозитории реализован REST API на Django REST Framework с набором viewset'ов и токенной аутентификацией.

- `api/serializers.py` — сериализаторы для API:
	- `FacultySerializer`, `DepartmentSerializer`, `ClassroomSerializer` — простые `ModelSerializer` для соответствующих моделей.
	- `DepartmentSerializer` использует вложенный `FacultySerializer` для чтения и `faculty_id` (write-only `PrimaryKeyRelatedField`) для записи.
	- `StudentGroupSerializer` использует вложенный `DepartmentSerializer` для чтения и `department_id` для записи.
	- `LessonSerializer` использует `StringRelatedField` для `teacher`, `group` и `Classroom` (отображает строковое представление связанных объектов). Поля: `fields = '__all__'`.
	- `NewsSerializer` помечает `author` как `StringRelatedField` и делает `author`, `created_at`, `updated_at` только для чтения при создании.
	- `UserSerializer` возвращает базовые поля пользователя и `role_display` через `get_role_display` и вложенную информацию о `group`.

- `api/views.py` — viewset'ы и логика доступа:
	- `FacultyViewSet`, `DepartmentViewSet`, `ClassroomViewSet`, `StudentGroupViewSet`, `NewsViewSet`, `LessonViewSet` реализованы как `ModelViewSet` и защищены `IsAuthenticated`.
	- `LessonViewSet.get_queryset()` ограничивает видимые занятия для студентов: если пользователь — студент и у него задана группа, API возвращает только уроки этой группы; иначе возвращается полный список, отсортированный по дню и времени.
	- `NewsViewSet.perform_create()` автоматически сохраняет `author=self.request.user` при создании новости.
	- `UserViewSet` реализован как `ViewSet` с экшеном `me` (`GET /api/profiles/me/`), который возвращает сериализованные данные текущего пользователя.

- `api/views_auth.py` — токенная аутентификация и выход:
	- `CustomAuthToken` (наследует `ObtainAuthToken`) в `post`-запросе валидирует логин/пароль и возвращает JSON с полями `token`, `user_id`, `username`, `role`, `first_name`, `last_name`, `group_id`.
	- `LogoutView` (APIView, `permission_classes = [IsAuthenticated]`) удаляет `request.user.auth_token` при POST-запросе, возвращая подтверждение выхода или ошибку.

- `api/urls.py` — маршруты API:
	- Регистрирует viewset'ы через `DefaultRouter`: `faculties`, `departments`, `classrooms`, `groups`, `lessons`, `news`, `profiles`.
	- Подключает маршруты аутентификации:
		- `POST /api/auth/login/` → `CustomAuthToken` (возвращает токен)
		- `POST /api/auth/logout/` → `LogoutView` (требует токен в заголовке, удаляет токен)
	- Полный набор эндпоинтов доступен под префиксом `/api/` (в `university/urls/main.py` этот роутер подключён как `path("api/", include(router.urls))`).

- `api/models.py` — пустой (в текущей версии дополнительных моделей для API нет).

Примеры запросов:

 - Получить уроки своей группы (студент):

```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/lessons/
```

 - Получение данных текущего пользователя:

```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/profiles/me/
```

 - Вход (получение токена):

```bash
curl -X POST -d "username=USER&password=PASS" http://127.0.0.1:8000/api/auth/login/
```

 - Выход (удаление токена):

```bash
curl -X POST -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/auth/logout/
```


### Шаблоны и статические файлы
- `templates/` — содержит `base.html`, `messages.html`, `schedule_table.html` и подпапки для приложений (`accounts/`, `public/`, `schedule/`).
	- `templates/schedule/pdf_raspisanie.html` — HTML-шаблон, используемый для генерации PDF экспорта.
- `static/` — CSS/JS и ресурсы фронтенда.
- `media/` — загружаемые файлы (аватары, изображения новостей и т.д.).

### Миграции
- В папках `*/migrations/` находятся autogenerated миграции (`0001_initial.py`, и т.д.). Не удаляйте их, они важны для воспроизводимости схемы.

---

## Советы по репозиторию
- Добавьте `.venv/` в `.gitignore`, если вы ещё этого не сделали, и удалите закоммиченный виртуальный env (в репе есть `.venv/` сейчас). Я могу помочь с командами для очистки истории (git rm -r --cached .venv && .gitignore update).
- Создайте `requirements.txt` (локально в виртуальном окружении):

```powershell
pip freeze > requirements.txt
```

- Заполните `university/settings/production.py` реальными продакшн-настроеками (секреты, DB URL, ALLOWED_HOSTS и т.д.).

## Что я могу сделать дальше
- Сгенерировать `requirements.txt` (хотите, чтобы я сделал это из текущего окружения?).
- Создать/обновить `.gitignore` (включая `.venv/`, `*.pyc`, `__pycache__`, `db.sqlite3`).
- Добавить примеры вызова API и пример CURL запроса к `/api/lessons/`.
- Добавить блок в README с диаграммой/скриншотами (пришлите изображения).

---

Если хотите, я сейчас могу автоматически:
- добавить `.venv/` в `.gitignore` и удалить уже закоммиченный `.venv` из индекса;
- или сгенерировать `requirements.txt`.

Напишите, что выполнить первым — сделаю и обновлю README при необходимости.


