'''Defines sample class and mid-level control structure
Written by Zach Flinkstrom and Ben Gincley'''
from picamera import PiCamera
import time
import os
import RPi.GPIO as GPIO
import image_processing
import datetime
import numpy as np
from scipy.misc import imsave

# Pin Setup:
VALVE = 18  # Valve pin number
valve_time = 1.5  # Valve open time in seconds
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(VALVE, False)  # Initiate valve as closed

def calibrate_preview():
    '''Opens a preview for user focusing, then takes series of pics
    for averaging and background subtraction'''
    with PiCamera() as camera:
        camera.resolution = (1664, 1232)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.2, 1.2)
        camera.framerate = 24
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()
        for i in range(10):
            output = np.empty((1232, 1664, 3), dtype=np.uint8)
            camera.capture(output, 'rgb')
            output = output/255.
            if i == 0:
                avg_image = output
            else:
                avg_image = (avg_image + output)/2.0
            time.sleep(0.1)
    return avg_image


def im_capture(bg):
    '''Cycles valve and captures an image to a numpy array'''
    if bg == False:
        GPIO.output(VALVE, True)
        time.sleep(valve_time)
        GPIO.output(VALVE, False)
        time.sleep(valve_time)
    with PiCamera() as camera:
        camera.resolution = (1664, 1232) 
        camera.awb_mode = 'off'
        camera.awb_gains = (1.2, 1.2)
        camera.framerate = 24
        output = np.empty((1232, 1664, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
    return output/255.


class Sample:
    '''Sample class to store information about each sample, which
    contains a series of device images and gets condensed into a single
    reading'''
    def __init__(self, sample_frequency, sample_volume, save_path,
                 save_images, save_images_path, bg):
        self.microbe_count = 0
        self.start_time = datetime.datetime.now()
        self.frames = 0
        self.sampled_vol = 0
        self.sample_volume = float(sample_volume)
        self.sample_time = sample_frequency
        self.save_path = save_path
        self.save = save_images
        self.save_im_path = save_images_path
        self.bg_avg = bg

    def add_pic(self):
        '''Captures and processes an image to the sample'''
        new_pic = im_capture(False)
        new_pic = new_pic - self.bg_avg
        self.frames += 1
        self.microbe_count += image_processing.process_image(new_pic, size=16)
        if  os.path.isabs(self.save_path) == False:
            os.mkdirs(self.save_path)
        if self.save == True:
            imsave('%s%s.png' % (self.save_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")), new_pic)


    def background_zero(self):
        bg_array = np.empty((0, 1232, 1640, 3))
        for i in range(50):
            bg_im = im_capture(True)
            bg_array.append((bg_im), axis=0)
            time.sleep(0.1)
        self.bg_avg = np.mean(bg_array, axis=0)


    def log(self):
        '''Writes .csv logfile with sample's results'''
        filename = '%s.csv' % self.save_path
        file_object = open(filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S,")
        concentration = self.microbe_count/self.sampled_vol
        file_object.write(now_string)
        file_object.write('Microbe count:,%d, ' % self.microbe_count +
                          'Sample Volume (uL):,%f,' % self.sampled_vol +
                          'Concentration (cells/uL):,%f,' % concentration + '\n')
        file_object.close()

    def sample_run(self):
        '''Loops to add pictures in allotted sample frequency or
        until a cell count threshold is reached'''
        loop_time = time.time()
        while (time.time() - loop_time) < self.sample_time and self.microbe_count < 10000:# or self.sampled_vol < self.sample_volume:
            t1 = time.time()
            self.add_pic()
            t2 = time.time()
            pictime = t2-t1
            self.sampled_vol += 0.00896 #Sampled volume in uL
            print('pic added in time %d' % pictime)
        while (time.time() - loop_time) < self.sample_time:
            time.sleep(0.1)
        self.log()
        print('logged result')
