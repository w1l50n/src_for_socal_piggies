#!/bin/bash

NAME="rapidsms_pi"                                   # Name of the application
DJANGODIR=/opt/pi/rapidsms_pi                # Django project directory
SOCKFILE=/tmp/rapidsms_gunicorn.sock              # we will communicte using this unix socket
USER=pi                                          # the user to run as
GROUP=pi                                          # the group to run as
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=rapidsms_pi.settings       # which settings file should Django use


echo "Starting $NAME"

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE \
  rapidsms_pi.wsgi

