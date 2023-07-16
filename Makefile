# run development server
runserver-dev:
	python manage.py runserver

# run make migrations and migrate for development server
makemigrations-migrate-dev:
	python manage.py makemigrations
	python manage.py migrate