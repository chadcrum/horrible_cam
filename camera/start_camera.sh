#!/bin/bash

#$CAM_URL=$1
#$CAM_NAME=$2

#ffmpeg -i 'rtsp://192.168.1.86:554/live/av0?user=admin&passwd=pylecam' -b 900k -vcodec copy -r 60 -y MyVdeoFFmpeg.avi
ffmpeg -y -i $CAM_URL -f image2 -updatefirst 1 /app/sd_cam/${CAM_NAME}.jpg
