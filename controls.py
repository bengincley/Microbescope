from picamera import PiCamera
import time
import os
import RPi.GPIO as GPIO
import image_processing
import datetime
import numpy as np
from scipy.misc import imsave

# Pin Setup:
LED = 12  # LED pin number
VALVE = 2  # Valve pin number
valve_time = 2
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(LED, False)
GPIO.output(VALVE, False)

def calibrate_preview():
    GPIO.output(LED, True)
    with PiCamera() as camera:
        camera.resolution = (1664, 1232)
        camera.awb_mode = 'off'
        camera.awb_gains = (1, 1)
        camera.framerate = 24
        time.sleep(30)
    GPIO.output(LED, False)

def im_capture():
    GPIO.output(LED, True)
    GPIO.output(VALVE, True)
    time.sleep(valve_time)
    GPIO.output(VALVE, False)
    time.sleep(valve_time)
    with PiCamera() as camera:
        camera.resolution = (1664, 1232) 
        camera.awb_mode = 'off'
        camera.awb_gains = (1, 1)
        camera.framerate = 24
        time.sleep(1)
        output = np.empty((1232, 1664, 3), dtype=np.uint8) 
        camera.capture(output, 'rgb')
    return np.mean(output, axis=2)


class Sample:
    def __init__(self, sample_frequency, save_path, save_images, save_images_path):
        self.microbe_count = 0
        self.start_time = datetime.datetime.now()
        self.frames = 0
        self.sample_time = sample_frequency
        self.save_path = save_path
        self.save = save_images
        self.save_im_path = save_images_path

    def add_pic(self):
        new_pic = im_capture()
        self.frames += 1
        self.microbe_count += image_processing.process_image(new_pic, size=30)
        if  os.path.isabs(self.save_path) == False:
            os.mkdirs(self.save_path)
        if self.save == True:
            imsave('%s%s.png' % (self.save_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")), new_pic)

    def log(self):
        filename = '%slogfile.csv' % self.save_path
        file_object = open(filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S:%f,")
        file_object.write(now_string)
        file_object.write('Microbe count:,%d, ' % self.microbe_count + '\n')
        file_object.close()

    def sample_run(self):
        loop_time = time.time()
        while (time.time() - loop_time) < self.sample_time and self.microbe_count < 400:
            self.add_pic()
        while (time.time() - loop_time) < self.sample_time:
            time.sleep(0.1)
        self.log()
