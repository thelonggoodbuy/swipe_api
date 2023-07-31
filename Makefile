# run development server
runserver-dev:
	export DJANGO_SETTINGS_MODULE=config.settings
	python manage.py runserver

# run make migrations and migrate for development server
makemigrations-migrate-dev:
	python manage.py makemigrations
	python manage.py migrate

# run all test with ignoring of deprecated warning
general-test-dev:
	export DJANGO_SETTINGS_MODULE=config.settings_test
	pytest -W ignore::DeprecationWarning --verbose