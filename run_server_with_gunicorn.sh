#!/bin/bash
NAME="trinity_api_server"                              #Name of the application (*)
DJANGODIR=/home/pi/Project/trinity/trinity_api_server             # Django project directory (*)
SOCKFILE=/home/pi/Project/trinity/run/gunicorn.sock        # we will communicate using this
USER=pi                                        # the user to run as (*)
GROUP=webdata                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes
DJANGO_SETTINGS_MODULE=trinity_api_server.settings             # which settings file should
DJANGO_WSGI_MODULE=trinity_api_server.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
source /home/pi/Project/trinity/myenv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do
# not use --daemon)
python $DJANGODIR/manage.py migrate
exec /home/pi/Project/trinity/myenv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user $USER \
    --bind=unix:$SOCKFILE
