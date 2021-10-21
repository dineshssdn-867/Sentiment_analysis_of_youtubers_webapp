web: bin/start-nginx bin/start-pgbouncer-stunnel gunicorn -c gunicorn.conf.py Sentiment_analysis_of_youtubers.wsgi --preload
worker: bin/start-pgbouncer-stunnel python manage.py qcluster