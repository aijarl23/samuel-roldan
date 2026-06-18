web: python manage.py migrate --settings=config.settings_prod && python setup_inicial.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2
