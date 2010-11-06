#! /bin/bash

NAME=supervisord
SUPERVISORD=/home/snswa/src/env/bin/supervisord
SUPERVISORCTL=/home/snswa/src/env/bin/supervisorctl
PIDFILE=/home/snswa/src/supervisord.pid
OPTS="-c /home/snswa/src/production/supervisord.conf"
PS=$NAME
TRUE=1
FALSE=0

test -x $SUPERVISORD || exit 0

export PATH="${PATH:+$PATH:}/usr/local/bin:/usr/sbin:/sbin:/home/snswa/src/env/bin:"

isRunning(){
    pidof_daemon
    PID=$?

    if [ $PID -gt 0 ]; then
	return 1
    else
        return 0
    fi
}

pidof_daemon() {
    PIDS=`pidof -x $PS` || true

    [ -e $PIDFILE ] && PIDS2=`cat $PIDFILE`

    for i in $PIDS; do
        if [ "$i" = "$PIDS2" ]; then
            return 1
        fi
    done
    return 0
}

start () {
    echo "Starting Supervisor daemon manager..."
    isRunning
    isAlive=$?

    if [ "${isAlive}" -eq $TRUE ]; then
        echo "Supervisor is already running."
    else
        $SUPERVISORD $OPTS || echo "Failed...!"
        echo "OK"
    fi
}

stop () {
    echo "Stopping Supervisor daemon manager..."
    $SUPERVISORCTL $OPTS shutdown ||  echo "Failed...!"
    echo "OK"
}

reload () {
    echo "Reloading Supervisor daemon manager..."
    isRunning
    isAlive=$?

    if [ "${isAlive}" -eq $TRUE ]; then
        $SUPERVISORCTL $OPTS reload || echo "Failed...!"
    else
        echo "Not running, starting..."
        start
    fi
}

case "$1" in
  start)
    start
	;;

  stop)
    stop
	;;

  restart)
    stop
    start
    ;;

  reload|force-reload)
    reload
    ;;

esac

exit 0
