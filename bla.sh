ffmpeg -i rtsp://192.168.1.10:554/s0-an -c:v copy -b:v 2000k -f dash -window_size 4 -extra_window_size 0 -min_seg_duration 2000000 -remove_at_exit 1 /opt/dash_test/html/webm_live/manifest.mpd

