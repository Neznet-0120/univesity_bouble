# University Double — Web platform for university

Brief project README for the Django web platform in this repository.

**Project Summary**
 - **Name:** `university_double`
 - **Type:** Django web application (university scheduling / information platform)
 - **Database:** SQLite (`db.sqlite3` included for development)
 - **Primary apps:** `accounts`, `core`, `groups_app`, `news`, `schedule`

**Quick Features**
 - **User accounts** and authentication (see `accounts` app).
 - **Schedule management** and export/printing views (see `schedule` app and templates).
 - **News and announcements** (see `news` app).
 - **Administrative interface** via Django admin; models registered in each app's `admin.py`.
 - **REST API**: a basic API is available in the `api` app (built with Django REST Framework).
 - **PDF export**: schedule export to PDF is available (uses `xhtml2pdf`) via an export endpoint (e.g. `accounts` has `export/pdf/`).

**Prerequisites**
 - Python 3.8+ (match your environment; project developed for standard Django 3.x/4.x workflows)
 - Git (optional)

**Recommended environment (Windows PowerShell)**
 1. Create and activate a virtual environment:

 ```powershell
 python -m venv .venv
 .\.venv\Scripts\Activate.ps1
 ```

 2. Install dependencies (add your `requirements.txt` if you have one). If you don't have a requirements file yet, install Django and common packages:

 ```powershell
 pip install --upgrade pip
 pip install django
 ```
```powershell
pip install djangorestframework xhtml2pdf
```

 3. Apply database migrations and create a superuser:

 ```powershell
 python manage.py migrate
 python manage.py createsuperuser
 ```

 4. Run development server:

 ```powershell
 python manage.py runserver
 ```

 Open `http://127.0.0.1:8000/` in a browser. Admin is at `http://127.0.0.1:8000/admin/`.

**Project layout (important files)**
 - `manage.py` : Django management entrypoint.
 - `db.sqlite3` : Default SQLite database for development.
 - `university/` : Django project package.
	 - `university/settings/` : `base.py`, `development.py`, `production.py` (environment-specific settings).
	 - `university/urls/` : main URL routing (`main.py`).
 - Apps:
	 - `accounts/` : user auth, forms, views, URLs.
	 - `core/` : core models and utilities.
	 - `groups_app/` : group-related models.
	 - `news/` : news articles and admin integration.
	 - `schedule/` : schedule models, views, and templates.
		- `api/` : serializers and viewsets for REST API endpoints (requires `djangorestframework`).
 - `templates/` : project templates including `base.html`, `schedule_table.html`, and app-specific subfolders.
 - `static/` and `media/` : static files and uploaded media.

**Settings & environment**
 - The repo includes `university/settings/development.py` and `production.py`. Use `development.py` for local work.
 - For secret keys and credentials, prefer environment variables or a `.env` file loaded by your settings (not included in the repo).

**Running tests**
 Run Django tests for all apps:

 ```powershell
 python manage.py test
 ```

 If you want to run tests for a specific app, add the app name: `python manage.py test accounts`.

**Static files & media**
 - Collect static files for production:

 ```powershell
 python manage.py collectstatic
 ```

 - During development, static files are served by Django when `DEBUG = True`.

**Deployment notes (high-level)**
 - Use a production-ready database (PostgreSQL or MySQL) instead of SQLite.
 - Serve static files via a CDN or web server (Nginx) after `collectstatic`.
 - Use a WSGI/ASGI server such as Gunicorn or Daphne behind Nginx.
 - Securely manage secrets using environment variables or a secret store.

**Contributing**
 - Add issues/feature requests to the repository tracker.
 - Follow the repository code style, open PRs against `main`, and describe the change clearly.

**Next steps / Suggestions**
 - Add a `requirements.txt` (run `pip freeze > requirements.txt` in your virtualenv) so other developers can install exact dependencies.
 - Add badges (CI, PyPI, license) at the top of this `README.md` if desired.
 - Provide a short developer setup script or Makefile (or PowerShell script) to automate common tasks.

**Contact / Author**
 - If you want this README customized (badges, license, screenshots, or deployment instructions), tell me what to include and I'll update it.

---

Generated: repository root `README.md` for the `university_double` Django project.

