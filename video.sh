#!/bin/bash

HOME=/opt/video
CONF=${HOME}/video.conf
IMAGES=${HOME}/images
VIDEOS=${HOME}/videos
LOGS=${HOME}/logs
SEGMENT_TIME=900


pkill -9 motion
pkill -9 ffmpeg

while read -r line;
do 
    name=$(echo $line | awk -F, '{print $1}')
    url=$(echo $line | awk -F, '{print $2}')
    echo $name
    echo $url
    if [ ! -d "${VIDEOS}/${name}" ]; then
        mkdir ${VIDEOS}/${name}
    fi
        
    ffmpeg -rtsp_transport tcp -loglevel debug -i $url -y -codec copy  -f segment -map 0 -segment_time $SEGMENT_TIME -strftime 1 "${VIDEOS}/${name}/${name}_%Y-%m-%d_%H-%M.mkv" -f image2 -updatefirst 1 ${IMAGES}/${name}.jpg </dev/null >/dev/null 2>${LOGS}/${name}.log &
     
done < $CONF

# Start up motion
motion -c /opt/video/motion/motion.conf
