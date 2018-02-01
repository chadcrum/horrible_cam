#!/bin/bash

# Kill all existing ffmpegs
ps -ef | grep ffmpeg | awk '{print $2}' | xargs -I{} kill -9 {}
pkill -9 ffmpeg
