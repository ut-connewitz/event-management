# event-management

Development repository for event management services.

## Overview
```
event-management/
├── Dockerfile
├── Dockerfile_deploy
├── OTHER
│   ├── db-model
│   │   ├── ERD_v2.png
│   │   ├── IDEF1X.dia
│   │   ├── IDEF1X.png
│   │   └── ut_db_schema.csv
│   ├── frontend-screenshots
│   │   ├── calendar_admin.png
│   │   ├── calendar_user.png
│   │   ├── login.png
│   │   ├── profile_page.png
│   │   ├── task_admin.png
│   │   └── task_user.png
│   ├── frontend.md
│   ├── plsql-scripts
│   │   ├── 01_ut_create_tables.sql
│   │   ├── 02_ut_index.sql
│   │   └── 03_ut_create_trigger.sql
│   └── use-cases.md
├── README.md
├── app
│   ├── backend
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── addbasedata.py
│   │   │       └── addtestdata.py
│   │   ├── migrations
│   │   ├── models
│   │   │   ├── event
│   │   │   ├── notification
│   │   │   ├── setting
│   │   │   ├── task
│   │   │   └── user
│   │   ├── templates
│   │   │   └── master.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── events
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── events_calendar
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── static
│   │   │   └── events_calendar
│   │   │       └── css
│   │   ├── templates
│   │   │   ├── events_calendar
│   │   │   │   ├── base.html
│   │   │   │   ├── calendar.html
│   │   │   │   ├── event_day.html
│   │   │   │   └── task.html
│   │   │   └── registration
│   │   │       └── login.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── manage.py
│   ├── profile_page
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── static
│   │   │   └── profile_page
│   │   │       └── css
│   │   ├── templates
│   │   │   ├── profile_page
│   │   │   │   ├── account.html
│   │   │   │   ├── adress.html
│   │   │   │   ├── base.html
│   │   │   │   └── profile_hub.html
│   │   │   └── registration
│   │   │       └── login.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static
│   │   └── css
│   │       └── base.css
│   ├── templates
│   │   └── base.html
│   └── testbootstrap
├── data
├── docker-compose-deploy.yml
├── docker-compose.yml
├── nginx
│   ├── Dockerfile
│   ├── default.conf
│   └── uwsgi_params
├── requirements.txt
└── scripts
    └── entrypoint.sh
```

## TODO

- Central database for all event related data (partially done).
- Web service for database administration.
- Web service for letting members of the UT-Connewitz select events where they want to participate.
- Server deploy.


## Framework

- [Django](https://docs.djangoproject.com): [4.2 LTS](https://www.djangoproject.com/download/)
- [Python: 3.11](https://docs.djangoproject.com/en/4.2/faq/install/#faq-python-version-support)
- [Bootstrap](https://pypi.org/project/django-bootstrap-v5/)
- SQL: Postgres


## Local-Docker-Dev-Setup
(*) *only needed for local IDE*

- (*) set up virtual env with Python 3.11 and Django 4.2
- clone into this repository
- (*) run `python3 -m pip install -r requirements.txt`
- run `docker compose up`
- run `docker exec events python3 manage.py makemigrations` & `docker exec events python3 manage.py migrate` to initialize local test db
- optionally run `docker exec events python3 manage.py addbasedata` & `docker exec events python3 manage.py addtestdata` to insert base and test data
- run `docker exec events python3 manage.py createsuperuser` to create admin user **fails due to: ``Superuser creation skipped due to not running in a TTY. You can run `manage.py createsuperuser` in your project to create one manually.``**
- run `docker compose exec events /bin/bash` to open the events container with CLI
- within the container: `python3 manage.py createsuperuser`
- open `http://0.0.0.0:8000/`

## Docker Deployment

1. Clone
2. create .env
3. Put the following
4. Change
```dotenv
DEBUG=False

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

ALLOWED_HOSTS=???????? #tbd
SECRET_KEY=samplesecret123
```

## IDEF1X model for the backend data structure
![IDEF1X](OTHER/db-model/IDEF1X.png)

## Frontend
### general development links
- Admin Interface: `http://0.0.0.0:8000/admin/`
- Calendar: `http://0.0.0.0:8000/ecal/calendar/`
- Profile Page: `http://0.0.0.0:8000/profile/hub/`
- Logout: `http://0.0.0.0:8000/accounts/logout/`

[Collection of current frontend screenshots](OTHER/frontend.md)
