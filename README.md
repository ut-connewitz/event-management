# event-management

Development repository for event management services.

## Overview
```
event-management/
├── Dockerfile
├── OTHER
│   ├── ERD_v2.png
│   ├── plsql-scripts
│   │   ├── 01_ut_create_tables.sql
│   │   ├── 02_ut_index.sql
│   │   └── 03_ut_create_trigger.sql
│   └── ut_db_schema - Tabellenblatt1.csv
├── README.md
├── app
│   ├── events
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
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


## DEV-Setup
(*) *only needed for local IDE*

- (*) set up virtual env with Python 3.11 and Django 4.2
- clone into this repository
- (*) run `python3 -m pip install -r requirements.txt`
- run `docker compose up`
- run `docker compose exec events /bin/bash`
- run `python3 manage.py makemigrations` & `python3 manage.py migrate` to initialize local test db
- run `python3 manage.py createsuperuser` to create admin user
- open `http://0.0.0.0:8000/`
