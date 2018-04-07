#!/bin/bash

CAM_LIST=record_names.txt
OUTPUT_DIR=/opt/horrible_cam/html/video

ps -ef | grep "$OUTPUT_DIR" | awk '{print $2}' | xargs -I{} kill -9 {}

for i in `cat $CAM_LIST`; do 
    FULL_OUT_DIR=${OUTPUT_DIR}/${i}
    mkdir -p $FULL_OUT_DIR
    nohup ffmpeg -i http://cams.boob.support:55444/${i}.webm -filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='%{localtime}': x=50: y=1: fontsize=10: fontcolor=yellow@0.8:" -vcodec libvpx -acodec copy -f segment -strftime 1 -segment_time 14400 -segment_format webm ${FULL_OUT_DIR}/${i}-%d_%m_%Y-%H_%M_%S.webm > /dev/null &
done

#http://cams.boob.support:55444/dining_room.webm


