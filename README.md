# event-management

Development repository for event management services.

## Overview
```
event-management/
├── Dockerfile
├── OTHER
│   ├── ERD_v2.png
│   ├── IDEF1X.dia
│   ├── IDEF1X.png
│   ├── plsql-scripts
│   ├── use-cases.md
│   └── ut_db_schema - Tabellenblatt1.csv
├── README.md
├── app
│   ├── backend
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── management
│   │   │   ├── __init__.py
│   │   │   └── commands
│   │   ├── migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
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
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── testbootstrap
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
- optionally run `python3 manage.py addbasedata` & `python3 manage.py addtestdata` to insert base and testdata
- run `python3 manage.py createsuperuser` to create admin user
- open `http://0.0.0.0:8000/`

## IDEF1X model for the backend data structure
![IDEF1X](OTHER/IDEF1X.png)
