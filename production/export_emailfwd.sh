#!/bin/bash

export PYTHONPATH=$HOME
export DJANGO_SETTINGS_MODULE=snswa_deploy.localsettings

export EMAILFWD_DATA=$HOME/emailfwd-data

mkdir -p ${EMAILFWD_DATA}
rm ${EMAILFWD_DATA}/*

exec $HOME/src/env/bin/django-admin.py export_emailfwd ${EMAILFWD_DATA}

$HOME/sync-emailfwd-data.sh
