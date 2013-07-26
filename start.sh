#!/bin/bash
 
NAME="prospop"                                  # Name of the application
DJANGODIR=/home/fareed/environments/prospop/prospop             # Django project directory
SOCKFILE=/home/fareed/environments/prospop/prospop/run/gunicorn.sock  # we will communicte using this unix socket
USER=fareed                                       # the user to run as
GROUP=fareed                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=prospop.settings             # which settings file should Django use
 
 
echo "Starting $NAME"
 
# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn_django \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  -b 0.0.0.0:8000
