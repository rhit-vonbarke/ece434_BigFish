# Dancing Fish

### ECE434 Final Project

This project uses the BeagleBone Black connected to a wired speaker to play music. The music is stored on the BeagleBone in .wav files after being downloaded from Youtube according to the user specifications. While the music is being played, two 8x8 LED matrices serve as a real-time visualizer and a dancing fish controlled by a servo is synchronized to the music.

More information about this project can be found at [ELinux](https://elinux.org/ECE434_Project:_Dancing_Fish) and [hackster.io](https://www.hackster.io/littlestpetcat/dancing-fish-caf63e).

### Setup Instructions 
To install and run the project, ssh into your Beaglebone and follow the instructions below:

1.) Clone this github repository

```bone$ git clone https://github.com/rhit-vonbarke/ece434_BigFish```

2.) Navigate to the project directory and run install.sh. This only needs to be run the first time that you are running the program as it installs all of the needed libraries.

```bone$ bash install.sh```

3.) Run setup.sh. This needs to be run every time after connecting to the bone before you want to run the program.

```bone$ bash setup.sh```

4.) Run the program (this needs to be rerun every time you want to play a new song).

```bone$ ```

5.) When prompted enter the link to the Youtube video you would like to listen to
