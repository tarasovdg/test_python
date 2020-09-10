#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
    echo "Running on http://0.0.0.0:5000/"
fi

python app.py create_db

python app.py seed_db

exec "$@"
