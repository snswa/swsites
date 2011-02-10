#!/bin/bash

export PYTHONPATH=$HOME
export DJANGO_SETTINGS_MODULE=snswa_deploy.localsettings

$HOME/src/env/bin/django-admin.py sync_emailfwd
