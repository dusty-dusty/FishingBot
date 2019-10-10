import mss
import numpy as np
from logging import getLogger, INFO
from logdna import LogDNAHandler
from time import sleep, strftime, time
from random import uniform, randint
from keyboard import wait, send, add_hotkey, on_press, is_pressed, press as kpress, release as krelease
from mouse import get_position, move, press, release, wheel
from cv2 import cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, imread, rectangle

'''
testing logging with logDNA.com
def enableLogger():
    loger = 'myapi'
    log = getLogger('logdna')
    log.setLevel(INFO)
    options = {
        'hostname': 'Python',
        'index_meta': True,
        'include_standard_meta': False,

    }
    logInput = LogDNAHandler(loger, options)
    log.addHandler(logInput)
    return log'''

def humanMove(numberX, numberY, randomMinimum=1, randomMaximum=1, minMove=1, maxMove=1):
    """Humanize moves the mouse cursor to a point on the screen."""
    try:
        x, y = get_position()
        randomNumber = randomValue(randomMinimum, randomMaximum)
        x2, y2 = (numberX - x) / randomNumber, (numberY - y) / randomNumber

        for number in range(randomNumber):
            moveSpeed = uniform(0.04, 0.09)
            offset = randint(minMove, maxMove)
            move(x2 + offset, y2 + offset, False, moveSpeed)

        move(numberX, numberY, duration=moveSpeed)
    except Exception as e:
        appendFile = open('logs/logfile_errors.txt', 'a')
        appendFile.write('ERROR(humanMove()) @{}  Info {}'.format(strftime("%c"), e))
        appendFile.close()


def humanMoverel(numberX, numberY, randomMinimum=0, randomMaximum=0, minMove=0, maxMove=0):
    """Humanize moves the mouse cursor to a point on the screen, relative to its current
    position."""
    randomNumber = randint(randomMinimum, randomMaximum)
    x, y = numberX / randomNumber, numberY / randomNumber

    for number in range(randomNumber):
        moveSpeed = uniform(0.04, 0.09)
        offset = randint(minMove, maxMove)

        move(x + offset, y, False, moveSpeed)


def humanClick(action):
    """ Sends a humanize click with the given button. """
    time_to_wait = uniform(0.032, 0.2)
    press(action)
    sleep(time_to_wait)
    release(action)
    #log.info("Clicked: {}".format(action)) testing log
    #print("test") testing log


def humanClickHold(action):
    """ Sends a humanize click with the given button. """
    time_to_wait = uniform(0.032, 0.2)
    press(action)
    sleep(time_to_wait)
    # release(action)


def humanClickRealse(action):
    """ Sends a humanize click with the given button. """
    time_to_wait = uniform(0.032, 0.2)
    # press(action)
    # sleep(time_to_wait)
    release(action)
    sleep(time_to_wait)


def humanKeyp(key):
    """ Humanize presses a given key. """
    time_to_wait = uniform(0.047, 0.2)
    kpress(key)
    sleep(time_to_wait)
    krelease(key)


def humanType(text):
    """ Humanize types a given words. """

    for letters in text:
        time_to_wait = uniform(0.047, 0.16)
        if letters.isupper():
            kpress('shift+{}'.format(letters.lower()))
            sleep(time_to_wait)
            krelease('shift+{}'.format(letters.lower()))
        else:
            kpress(letters)
            sleep(time_to_wait)
            krelease(letters)


def grabPixel(numberX, numberY):
    """ Grabs a pixel colour on a point of the screen."""
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[1])

        return sct_img.pixel(numberX, numberY)


def randomValue(valueMin, absValue, offset=0):
    """Random int maker that makes sure min value is not greater than the absolute value"""
    if absValue + offset < 0:
        offset = 0
    if absValue < valueMin:
        valueMin = 0

    absValue += offset
    return randint(valueMin, absValue)


def pixelMatchesColor(colour, match, tolerance=0):
    """Matches a pixel colour on a point of the screen."""
    # should always be 3 or 4 (rbg, possibly with an alpha channel)
    if colour == match:  # exact match
        return True
    has_matched = True
    if tolerance > 0:
        for index in range(len(colour)):  # make sure all 3 match
            if colour[index] - tolerance > match[index]:  # too high
                has_matched = False
            elif colour[index] + tolerance < match[index]:  # too low
                has_matched = False
    if has_matched:
        return True
    else:
        return False


def pixelFindColour(colour, numberX, numberY, numberXMax, numberYMax, tolerance=0, boolValue=False):
    """Finds and Matches a pixel colour on screen."""
    box = {
        "left": numberX,
        "top": numberY,
        "width": numberXMax - numberX,
        "height": numberYMax - numberY,
    }
    with mss.mss() as sct:
        img = sct.grab(box)
        pixels = zip(img.raw[2::4], img.raw[1::4], img.raw[0::4])

        for checked, matchFind in enumerate(pixels):
            # print(matchFind)
            if matchFind == colour:  # exact match
                areaHeight = int(checked / box["width"])
                totalArea = checked - (areaHeight * box["width"])  # removes checked pixles from total pixels
                x = numberX + totalArea
                y = numberY + areaHeight
                if boolValue:
                    return True
                else:
                    print("found match = {} {}".format((x, y), colour))
                    return x, y
            elif tolerance > 0:
                hasMatched = True
                for index in range(len(colour)):  # make sure all r,g,b match all 3
                    if colour[index] - tolerance > matchFind[index]:  # too high
                        hasMatched = False
                    elif colour[index] + tolerance < matchFind[index]:  # too low
                        hasMatched = False
                if hasMatched:
                    areaHeight = int(checked / box["width"])
                    totalArea = checked - (areaHeight * box["width"])  # removes checked pixles from total pixels
                    x = numberX + totalArea
                    y = numberY + areaHeight

                    if boolValue:
                        return True
                    else:
                        print("tolerance found match = {} {}".format((x, y), colour))
                        return x, y

        # print('Search done no match, retry!')
        return False


def imageLocation(numberX=None, numberY=None, numberXMax=None, numberYMax=None):
    with mss.mss() as sct:
        if numberX is None:
            box = sct.monitors[1]
        else:
            box = {
                "left": numberX,
                "top": numberY,
                "width": numberXMax - numberX,
                "height": numberYMax - numberY,
            }
        return sct.grab(box)


def imageFind(matchImage, screenImage, numberX=None, numberY=None, tolerance=0.7, imageShape=0, boolValue=False):
    """Finds and matches images on a the screen."""
    try:
        img_rgb = np.array(screenImage)
        img_gray = cvtColor(img_rgb, COLOR_BGR2GRAY)
        template = imread(matchImage, 0)

        res = matchTemplate(img_gray, template, TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = minMaxLoc(res)
        x = max_loc[0] + numberX
        y = max_loc[1] + numberY
        xShapeSize = template.shape[1]
        yShapeSize = template.shape[0]
        if boolValue:
            if max_val < tolerance:
                return False
            else:
                return True
        if imageShape is 1:
            if max_val < tolerance:
                return 0, 0, 0, 0
            else:
                return x, y, xShapeSize, yShapeSize
        if max_val < tolerance:
            return 0, 0
        else:
            return x, y
    except Exception as e:
        appendFile = open('logs/logfile_errors.txt', 'a')
        appendFile.write('ERROR(imageFind()) @{}  img:{} Info {}'.format(strftime("%c"), matchImage, e))
        appendFile.close()

#log = enableLogger()
