#!/usr/bin/python3

import os
import subprocess
import shutil
import time
import signal
import filecmp


IMAGE_DIR = os.path.join("/media", os.environ.get("USER"))
DELAY = 2
WALLPAPER = os.path.join(os.path.expanduser("~"), 'wallpaper.jpg')
current_path = os.path.dirname(os.path.realpath(__file__))
IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'}
wall_process = None


SLIDESHOW_CMD = [
    'feh',
    '--recursive',
    '--fullscreen',
    '--reverse',
    '--sort', 'mtime',
    '--auto-zoom',
    '--hide-pointer',
    '--slideshow-delay'
]

WALLPAPER_CMD = [
    'feh',
    '--fullscreen',
    '--zoom', 'fill',
    '--hide-pointer',
    WALLPAPER
]

images_path = None


def copy_wallpaper(wall_location):
    user_wallpaper = os.path.join(wall_location, "wallpaper.jpg")
    if os.path.isfile(user_wallpaper):
        if not filecmp.cmp(user_wallpaper, WALLPAPER):
            shutil.copyfile(user_wallpaper, WALLPAPER)


def read_cfg(cfg_location):
    global DELAY

    config_file_path = os.path.join(cfg_location, 'config.txt')

    if os.path.isfile(config_file_path):
        try:
            config_file = open(config_file_path, "r")
            lines = config_file.readlines()
            for line in lines:
                data = line.strip()
                if not data.startswith("#"):
                    cfg_line = data.split("=")
                    if len(cfg_line) == 2:
                        var_name = cfg_line[0].strip()
                        var_val = cfg_line[1].strip()

                        if var_name == "delay":
                            try:
                                DELAY = int(var_val)
                            except Exception as ve:
                                print(f"ERROR: {ve}")
                                DELAY = 2
                            break

            config_file.close()
        except Exception as e:
            print(f"{config_file_path} not accessible")


def check_img_available(path=IMAGE_DIR):
    global images_path

    if images_path is None:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                check_img_available(full_path)
            else:
                ext = entry.split(".")[1].lower().strip()
                if ext in IMAGE_EXTENSIONS:
                    images_path = path


def run_slideshow(img_path):
    try:
        command = SLIDESHOW_CMD.copy()
        command.append(f"{DELAY}")
        command.append(img_path)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        pass


def show_wallpaper():
    global wall_process

    wall_process = subprocess.Popen(WALLPAPER_CMD)


source = os.path.join(current_path, 'wallpaper.jpg')
if not os.path.isfile(WALLPAPER):
    shutil.copyfile(source, WALLPAPER)

while True:
    images_path = None
    check_img_available()

    if images_path is not None:
        if wall_process:
            os.kill(wall_process.pid, signal.SIGTERM)
            wall_process = None

        # Check if a wallpaper image is inserted
        copy_wallpaper(images_path)
        read_cfg(images_path)
        run_slideshow(images_path)
    else:
        if wall_process is None:
            show_wallpaper()

    time.sleep(2)
