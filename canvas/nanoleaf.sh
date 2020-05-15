#!/bin/bash

CWD=`dirname $0`
PIDFILE=/tmp/nanoleaf.pid

start()
{
    $CWD/nanoleaf.py > /dev/null 2>&1 &
    mypid=$!
    echo $mypid > $PIDFILE
}

stop()
{
    if [ -s $PIDFILE ]; then
        mypid=`cat $PIDFILE`
        kill $mypid
        rm -f $PIDFILE
    fi
}

if [ "$1" == "start" ]; then
    stop
    start
fi

if [ "$1" == "stop" ]; then
    stop
fi