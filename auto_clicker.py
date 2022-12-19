from os import walk
from os.path import join
import numpy as np
import cv2
import pyautogui
from simpleobject import simpleobject as so
from time import sleep

IMAGES = 'images'
THRESHOLD = 0.9

pyautogui.FAILSAFE = False

def get_images():
    images = so()
    for root, dirs, files in walk(IMAGES):
        for file in files:
            split = file.rsplit('.', 1)
            if len(split) == 2:
                name, extension = split
                if name and extension:
                    path = join(root, file)
                    images[name] = cv2.imread(path)
    return images

def find_image(template, image=None):
    if image is None:
        image = screenshot()
    w, h, _ = template.shape
    match = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    if np.amax(match) > THRESHOLD:
        top_left = cv2.minMaxLoc(match)[3]
        x = top_left[0] + w//2
        y = top_left[1] + h//2
        return x, y

def click_image(template, image=None):
    if image is None:
        image = screenshot()
    if pos := find_image(template, image):
        old_pos = pyautogui.position()
        pyautogui.click(*pos)
        pyautogui.moveTo(old_pos)
        return True
    return False

def screenshot():
    pil_img = pyautogui.screenshot()
    np_array = np.array(pil_img)
    cv_img = cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR)
    return cv_img

def main():
    images = get_images()
    try:
        while True:
            for name, image in images.items():
                if click_image(image):
                    print('clicked', name)
                    break
            sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()