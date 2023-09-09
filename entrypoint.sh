#!/bin/sh


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL starter"
fi

# python manage.py flush --no-input
echo "************************************************************"
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
echo "============================================================"

exec "$@"