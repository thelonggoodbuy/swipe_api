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

# echo "-----------STATIC------------------"
# echo yes | python manage.py collectstatic
# echo "-------END-STATIC------------------"

# python manage.py users_initial_script
# python manage.py house_initial_script
# python manage.py ads_initial_script
echo "============================================================"

exec "$@"