web: python manage.py collectstatic --noinput && python manage.py migrate && python setup_inicial.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2
