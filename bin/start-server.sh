#!/bin/sh
set -e

if [ "$APP_ENV" = "dev" ]; then
  echo "Starting development server"
  FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run --host=0.0.0.0
elif [ "$APP_ENV" = "test" ]; then
  echo "Starting test server"
  FLASK_APP=app.py FLASK_DEBUG=0 python -m flask run --host=0.0.0.0
else
  echo "Starting production server"
  FLASK_APP=app.py FLASK_DEBUG=0 python -m flask run --host=0.0.0.0
fi
