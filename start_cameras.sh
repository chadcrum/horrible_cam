#!/bin/sh


nohup ffserver -f /opt/ffserver/ffserver_chad.conf 2>&1 &

nohup while true; sleep 5; do ffmpeg -rtsp_transport tcp -i rtsp://admin:yourmom%21@192.168.1.252:554/videoMain -probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/backyard_porch.ffm ; sleep 10; done 2>&1 &

nohup ffmpeg -rtsp_transport tcp -i rtsp://admin:yourmom%21@192.168.1.252:554/videoMain -probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/backyard_porch.ffm  2>&1 &
nohup ffmpeg -rtsp_transport tcp -i rtsp://admin:yourmom%21@192.168.1.94:554/videoMain -probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/backyard_fence.ffm  2>&1 &
nohup ffmpeg -rtsp_transport tcp -i "rtsp://192.168.1.86:554/live/av0?user=admin&passwd=pylecam" -probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/dining_room.ffm 2>&1 &
nohup ffmpeg -rtsp_transport tcp -i "rtsp://192.168.1.250:554/live/av0?user=admin&passwd=pylecam" -probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/living_room.ffm 2>&1 &
nohup ffmpeg -rtsp_transport tcp -i "rtsp://192.168.1.70:554/live/av0?user=admin&passwd=pylecam" --probesize 128 -analyzeduration 500 -max_muxing_queue_size 690 http://localhost:8090/kitchen.ffm 2>&1 &
nohup ffmpeg  -i rtsp://192.168.1.213:554/s0 http://localhost:8090/drive_way.ffm 2>&1 &
