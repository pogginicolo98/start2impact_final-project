#!/bin/bash

NAME="PROJECT_NAME"
DJANGODIR=/home/USERNAME/PROJECT_DIR/PROJECT_NAME
SOCKFILE=/home/USERNAME/PROJECT_DIR/VIRTUAL_ENVIRONMENT/run/gunicorn.sock
USER=USERNAME
GROUP=USERNAME
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=PROJECT_NAME.settings
DJANGO_WSGI_MODULE=PROJECT_NAME.wsgi
echo "Starting $NAME as `whoami`"


cd $DJANGODIR
source /home/USERNAME/PROJECT_DIR/VIRTUAL_ENVIRONMENT/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
