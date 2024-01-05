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
- Docker integration.
- Server deploy.


## Framework

- [Django](https://docs.djangoproject.com): [4.2 LTS](https://www.djangoproject.com/download/)
- [Python: 3.11](https://docs.djangoproject.com/en/4.2/faq/install/#faq-python-version-support)
- [Bootstrap](https://pypi.org/project/django-bootstrap-v5/)
- SQL: Postgres


## Set-Up

- (set up virtual env with Python 3.11 and Django 4.2)
- clone into this repository
- go to `event-management/events/` directory
- run `manage.py makemigrations` &
- run `manage.py migrate to initialize local test db
- run `python manage.py runserver`
- (open `http://127.0.0.1:8000/` / `http://localhost:8000` -> 404)
- open `http://localhost:8000/polls/` for hello world

## Docker WIP

- **there are several issues with that atm, so its not really working but might be helpful for testing and finding an actual setup**

- go to `event-management/events/` directory
- run `docker compose up`
- mocked db container and container for project should be build and run

