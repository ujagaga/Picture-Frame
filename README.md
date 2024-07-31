# Picture-Frame
Linux automatic slideshow preview images.
My requirements:
- lightweight
- start fullscreen slideshow as soon as a USB flash is inserted
- always in fullscreen mode whether images are available or not
- slideshow delay up to few days

## How it works
A python script checks contents of /media/$USER/. If empty (no external media connected) show "wallpaper.jpg". 
As soon as USB flash is mounted, start the slideshow. Sorting is based on modify date, 
so the latest images are displayed first. 

To change the wallpaper, just copy an image on the flash drive and name it "wallpaper.jpg". 
It will be used as wallpaper when no external media is present.

Default slideshow delay is 2 seconds. To change it, just create a "config.txt" on your external media
and write new delay like:

        delay=1234

Any other content will be ignored

The script uses "Feh" image viewer in the background.

## How to start
1. Prepare a linux with minimal X server or X11-compatible environment.
2. Make sure you have Python 3 installed
3. Run the install script

NOTE:
The install script is written for Ubuntu. It uses system service to run the python script at startup.
If you want to run this in a different environment, you just need to install Feh, Python3 and 
run the script at startup.
