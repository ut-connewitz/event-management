# event-management

Development repository for event management services.

## Overview
```
.
├── README.md
└── events [project directory]
    ├── Dockerfile
    ├── db.sqlite3
    ├── docker-compose.yml 
    ├── events [project setup files]
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── settings.cpython-311.pyc
    │   │   ├── urls.cpython-311.pyc
    │   │   └── wsgi.cpython-311.pyc
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py [central django file for managing the project]
    ├── polls [app directory with app setup files -> own repository?]
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── models.cpython-311.pyc
    │   │   ├── testPolls.cpython-311.pyc
    │   │   ├── testPost.cpython-311.pyc
    │   │   ├── tests.cpython-311.pyc
    │   │   ├── urls.cpython-311.pyc
    │   │   └── views.cpython-311.pyc
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

