release: python manage.py migrate --no-input
web: gunicorn agilbot.wsgi:application --log-file -
