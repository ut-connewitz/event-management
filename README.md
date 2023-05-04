# event-management

Development repository for event management services.

## TODO:

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
- go to `/events/` directory
- run `python manage.py runserver`
- (open `http://127.0.0.1:8000/` / `http://localhost:8000` -> 404)
- open `http://localhost:8000/polls/` for hello world
