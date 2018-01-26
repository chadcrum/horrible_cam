# Use an official Python runtime as a base image
FROM ubuntu:16.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Define mountable directories.
VOLUME ["/app"]

# Install any needed packages specified in requirements.txt
#RUN apt -y update && apt install -y software-properties-common && add-apt-repository -y ppa:jonathonf/ffmpeg-3 && apt update -y && apt install ffmpeg -y
RUN apt -y update && apt install -y software-properties-common && add-apt-repository -y ppa:jonathonf/ffmpeg-3 && apt install ffmpeg -y

# Run app.py when the container launches
CMD ./start_camera.sh ${CAM_URL} ${CAM_NAME}

