from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import datetime
import numpy as np
import scipy as sp
from PIL import Image

# Pin Setup:
LED = 1 #Pin#
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)


with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.awb_mode = 'off'
    camera.awb_gains = (1, 1)
    output = np.empty((1920, 1080, 3), dtype=np.uint8)
    camera.start_preview()
    sleep(3)
    GPIO.output(LED, True)
    sleep(10)
    camera.capture(output, 'rgb')
    #output = output[:, :3280, :] # strip off uninitialized pixels
    GPIO.output(LED, False)
    sleep(3)
    camera.stop_preview()
    im = Image.fromarray(output)
    im.save("/home/pi/Desktop/image1.jpeg")
