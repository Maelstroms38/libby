# pull official base image
FROM python:3.8.3-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1
ENV HEROKU_APP_NAME libby-app

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN apt-get install -y python3-pip

RUN pip install pipenv

# install dependencies
COPY Pipfile* /app
RUN cd /app && pipenv lock --requirements > requirements.txt
RUN pip install -r /app/requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# migrate database
RUN python manage.py migrate

# run gunicorn
CMD gunicorn library.wsgi:application --bind 0.0.0.0:$PORT