#!/bin/bash


sudo apt update
sudo apt -y install feh

SERVICE_NAME=pictureframe.service
SERVICE_FILE=/etc/systemd/system/$SERVICE_NAME

# Disable existing service if any
sudo systemctl disable $SERVICE_NAME

# Create new startup service
{
echo "[Unit]"
echo Description=Image slideshow app
echo
echo "[Service]"
echo Type=simple
echo RemainAfterExit=yes
echo User=$USER
echo Group=$USER
echo Restart=always
echo RestartSec=10s
echo ExecStart=$PWD/pictureframe.py
echo WorkingDirectory=$PWD
echo
echo "[Install]"
echo WantedBy=multi-user.target
} > temp.service
sudo mv temp.service $SERVICE_FILE

# Enable service
sudo systemctl enable $SERVICE_NAME

