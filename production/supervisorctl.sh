#!/bin/bash

SUPERVISORCTL=/home/snswa/src/env/bin/supervisorctl
OPTS="-c /home/snswa/src/production/supervisord.conf"

$SUPERVISORCTL $OPTS $@
