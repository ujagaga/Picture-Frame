#!/bin/bash


sudo apt update
sudo apt -y install feh

chmod +x $PWD/pictureframe.py
mkdir -p "$HOME/.config/autostart"
SHORTCUT="$HOME/.config/autostart/pictureframe.desktop"
echo "Creating shortcut file: $SHORTCUT"

{
echo "[Desktop Entry]"
echo "Version=1.1"
echo "Type=Application"
echo "Name=Picture Frame"
echo "Comment=USB Flash Slideshow"
echo "Exec=$PWD/pictureframe.py"
echo "Categories=Utility;"
} > $SHORTCUT

