#!/bin/sh
python /app/manage.py migrate #todo: reavaliar a execução automática
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi \
  -k gevent \
  -w $(python -c "import multiprocessing; print(2 * multiprocessing.cpu_count())") \
  -b 0.0.0.0:5000 \
  --chdir=/app \
  --log-level=$DJANGO_LOG_LEVEL \
  --timeout=0

