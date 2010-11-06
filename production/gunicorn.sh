#!/bin/bash

export PYTHONPATH=$HOME
export DJANGO_SETTINGS_MODULE=snswa_deploy.localsettings

exec env/bin/gunicorn_django \
    --log-file=/home/snswa/logs/gunicorn_public.log \
    --bind=127.0.0.1:20000 \
    --workers=2 \
    /home/snswa/snswa_deploy/localsettings.py
