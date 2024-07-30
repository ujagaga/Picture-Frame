#!/usr/bin/python3

import os
import subprocess
import shutil
import time
import signal


CFG_FILE = os.path.join(os.path.expanduser("~"), 'pictureframe.cfg')
IMAGE_DIR = os.path.join("media", os.getlogin())
DELAY = 2
WALLPAPER = os.path.join(os.path.expanduser("~"), 'wallpaper.jpg')
current_path = os.path.dirname(os.path.realpath(__file__))
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
wall_process = None


SLIDESHOW_CMD = [
    'feh',
    '--recursive',
    '--fullscreen',
    '--preload',
    '--reverse',
    '--slideshow-delay', '2',
    '--sort', 'mtime',
    '--auto-zoom',
    IMAGE_DIR
]

WALLPAPER_CMD = [
    'feh',
    '--fullscreen',
    '--zoom', 'fill',
    WALLPAPER
]


def move_wallpaper(wall_location):
    user_wallpaper = os.path.join(wall_location, "wallpaper.jpg")
    if os.path.isfile(user_wallpaper):
        shutil.move(user_wallpaper, WALLPAPER)


def read_cfg():
    global IMAGE_DIR
    global DELAY
    global SLIDESHOW_CMD
    global WALLPAPER_CMD

    if os.path.isfile(CFG_FILE):
        try:
            config_file = open(CFG_FILE, "r")
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

            config_file.close()
        except Exception as e:
            print(f"{CFG_FILE} not accessible")
    else:
        print(f"The config file '{CFG_FILE}' does not exist. Creating one.")
        with open(CFG_FILE, "w") as cfg_file:
            cfg_file.write(f"delay={DELAY}\n")

    source = os.path.join(current_path, 'wallpaper.jpg')
    if not os.path.isfile(WALLPAPER):
        shutil.copyfile(source, WALLPAPER)


def check_img_available():
    if os.path.isdir(IMAGE_DIR):
        for item in os.listdir(IMAGE_DIR):
            item_path = os.path.join(IMAGE_DIR, item)
            if os.path.isdir(item_path):
                for filename in os.listdir(item_path):
                    if os.path.isfile(os.path.join(item_path, filename)):
                        ext = os.path.splitext(filename)[1].lower()
                        if ext in IMAGE_EXTENSIONS:
                            return item_path
    return None


def run_slideshow(img_path):
    try:
        command = SLIDESHOW_CMD.copy()
        command.append(img_path)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        pass


def show_wallpaper():
    global wall_process

    wall_process = subprocess.Popen(WALLPAPER_CMD)


read_cfg()

while True:
    images_path = check_img_available()
    if images_path is not None:
        if wall_process:
            os.kill(wall_process.pid, signal.SIGTERM)
            wall_process = None

        # Check if a wallpaper image is inserted
        move_wallpaper(images_path)

        run_slideshow(images_path)
    else:
        if wall_process is None:
            show_wallpaper()

    time.sleep(2)
