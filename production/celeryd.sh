#!/bin/bash

export PYTHONPATH=$HOME
export DJANGO_SETTINGS_MODULE=snswa_deploy.localsettings

exec $HOME/src/env/bin/django-admin.py celeryd \
    --settings=snswa_deploy.localsettings \
    -c1 -B -E -linfo
