# event-management

Development repository for event management services.

## Overview
```
.
├── README.md
├── db-model [information/blueprints]
│   ├── ERD_v2.png
│   ├── plsql-scripts 
│   │   ├── 01_ut_create_tables.sql
│   │   ├── 02_ut_index.sql
│   │   └── 03_ut_create_trigger.sql
│   └── ut_db_schema - Tabellenblatt1.csv
└── events [project directory]
    ├── Dockerfile
    ├── db.sqlite3
    ├── docker-compose.yml 
    ├── events [project setup files]
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py [central django file for managing the project]
    ├── polls [app directory with app setup files -> own repository?]
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   │   ├── __init__.py
    │   │   └── __pycache__
    │   │       └── __init__.cpython-311.pyc
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    └── requirements.txt [dependencies]
```

## TODO

- Central database for all event related data (partially done).
- Web service for database administration.
- Web service for letting members of the UT-Connewitz select events where they want to participate.
- Docker integration.
- Server deploy.


## Framework

- [Django](https://docs.djangoproject.com): [4.2 LTS](https://www.djangoproject.com/download/)
- [Python: 3.11](https://docs.djangoproject.com/en/4.2/faq/install/#faq-python-version-support)
- [Bootstrap](https://pypi.org/project/django-bootstrap-v5/)
- SQL: tbd


## Development Set-Up

*Prerequisites: Python 3.11*

1. Clone repo
2. Create/Activate virtual env (`python3 -m venv venv` & `source venv/bin/activate`)
3. Install dependencies (`pip install -r requirements.txt`)

- go to `event-management/events/` directory
- run `manage.py makemigrations` &
- run `manage.py migrate to initialize local test db
- run `python manage.py runserver`
- (open `http://127.0.0.1:8000/` / `http://localhost:8000` -> 404)
- open `http://localhost:8000/polls/` for hello world

## Deploy Docker

1. Go to the root of the repo `event-management/`
2. Run `docker compose up`
3. Access Frontend on http://localhost:8000