import mss
import numpy
import threading
from winsound import PlaySound, SND_ASYNC
from PIL import ImageGrab
from time import sleep, strftime, time, clock
from random import uniform, randint
from keyboard import wait, send, add_hotkey, on_press, is_pressed, press as kpress, release as krelease, read_key, \
    on_press_key, on_release_key
from mouse import get_position as getPos, move, press, release, click, drag, wheel
from humanize_zucc import *
from cv2.cv2 import cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, imread, COLOR_BGR2GRAY, \
    imshow, line, IMREAD_COLOR

a = 0

if a == 1:
    for i in range(1000):
        img = imageLocation(667, 377, 927, 681)
        x, y, xMax, yMax = imageFind('images/npcdismiss.png', img, 667, 377, tolerance=0.6, imageShape=1)
        if x > 0:
            print("Found my name")
            humanMove((x + xMax / 2), (y + yMax), 3, 5, -10, 10)
            sleep(1)


def grabPixels(pixelX, pixelY):
    """ Grabs a pixel colour on a point of the screen."""
    try:
        return ImageGrab.grab().load()[pixelX, pixelY]
    except Exception as e:
        print('#ERROR Info {}\n'.format(e))
        # pass


def finder():
    print("started")
    key = "q"
    on_off = 0
    while True:
        try:
            if is_pressed(key):
                if on_off == 0:
                    on_off = 1
                    # colour's = grabPixels(714, 78)
                    # print('colour's #1: {}'.format(colour's))
                    print('mouse pos #1: {}'.format(getPos()))
                    x, y = getPos()
                    start = time()
                    colour = grabPixels(x, y)
                    print(time() - start)
                    print('colour #1: {}'.format(colour))
                elif on_off == 1:
                    on_off = 0
                    print('\nmouse pos #2: {}'.format(getPos()))
                    [xMax, yMax] = getPos()
                    start = time()
                    colour = grabPixels(xMax, yMax)
                    print(time() - start)
                    print('colour #2: {}\n'.format(colour))
                    print('Full Pos: {}, {}, {}, {}\n'.format(x, y, xMax, yMax))
                while is_pressed(key):
                    sleep(0.01)
        except Exception as e:
            print("#ERROR debug Info {}\n".format(e))
        else:
            sleep(0.01)


finders = threading.Thread(target=finder)
finders.start()
