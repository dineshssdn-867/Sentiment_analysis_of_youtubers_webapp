web: bin/start-nginx bin/start-pgbouncer-stunnel gunicorn -c gunicorn.conf.py Fantom.wsgi --preload
worker: bin/start-pgbouncer-stunnel python manage.py qcluster