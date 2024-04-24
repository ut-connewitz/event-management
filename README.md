# event-management

Development repository for event management services.

## Overview
```
event-management/
├── Dockerfile
├── OTHER
│   ├── ERD_v2.png
│   ├── IDEF1X.png
│   ├── plsql-scripts
│   │   ├── 01_ut_create_tables.sql
│   │   ├── 02_ut_index.sql
│   │   └── 03_ut_create_trigger.sql
│   └── ut_db_schema - Tabellenblatt1.csv
├── README.md
├── app
│   ├── events
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── testbootstrap
│       ├── __init__.py
│       ├── __pycache__
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       ├── models.py
│       ├── templates
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── data
│   └── db
├── docker-compose.yml
└── requirements.txt
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
- run `docker exec events python3 app/manage.py makemigrations` & `docker exec events python3 app/manage.py migrate` to initialize local test db
- run `docker exec events python3 app/manage.py createsuperuser` to create admin user
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
