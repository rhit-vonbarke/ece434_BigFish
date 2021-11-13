#!/bin/bash

echo "Installing necessary libaries, this may be slow:"
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
sudo apt install software-properties-common
sudo apt update
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt install ffmpeg
mkdir "audiodownloads"
#test code; comment out later
youtube-dl -x --audio-format wav https://www.youtube.com/watch?v=diSjU2Go1mM
