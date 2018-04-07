#!/bin/bash
if [ -z "$STY" ]; then exec screen -dm -S ffserver /bin/bash "$0"; fi
ffserver -f ffserver_chad.conf
