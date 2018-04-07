#!/bin/bash

CAM_LIST=camera_list.txt

# Kill all existing ffmpegs
ps -ef | grep ffmpeg | awk '{print $2}' | xargs -I{} kill -9 {}
pkill -9 ffmpeg

IFS=$'\n'

for cam in `cat $CAM_LIST`;
do
    nohup bash -c "while true; do sleep 2; $cam; sleep 5; done" > /dev/null &
    #nohup bash -c "$cam > /dev/null &"
done
