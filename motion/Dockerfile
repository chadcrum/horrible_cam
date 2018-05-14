FROM ubuntu:16.04

RUN apt update && apt -y install wget 
#RUN wget https://github.com/Motion-Project/motion/releases/download/release-4.1.1/trusty_motion_4.1.1-1_amd64.deb
RUN wget https://github.com/Motion-Project/motion/releases/download/release-4.1.1/xenial_motion_4.1.1-1_amd64.deb 
RUN dpkg -i xenial_motion_4.1.1-1_amd64.deb; apt-get -fy install
#RUN apt-get -fy install
#RUN dpkg -i trusty_motion_4.1.1-1_amd64.deb
#CMD cd /etc/motion && motion -c motion.conf
CMD motion
