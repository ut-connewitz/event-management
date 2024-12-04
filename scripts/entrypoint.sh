#!/bin/sh

echo "
    web service for event management
    Copyright (C) 2024  franziskusz, JohannesGGE and contributers
    Contact: 79016562+franziskusz@users.noreply.github.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    "

set -e

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

#python manage.py createsuperuser --noinput #comment out after first deploy

python manage.py addbasedata

python manage.py addtestdata #remove for production deploy

uwsgi --socket :44444 --master --enable-threads --module events.wsgi
