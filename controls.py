'''Defines sample class and mid-level control structure
Written by Zach Flinkstrom and Ben Gincley'''
import picamera
import time
import os
import RPi.GPIO as GPIO
import image_processing
import datetime
import numpy as np
import unicornhathd as pihat
from scipy.misc import imsave

# Pin Setup:
VALVE = 18  # Valve pin number
valve_time = 1.0  # Valve open time in seconds
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(VALVE, False)  # Initiate valve as closed
display = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1],
         [1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 1, 1, 1],
         [1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1],
         [1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1],
         [1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1],
         [1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1],
         [1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
display = np.array(display)

def calibrate_preview():
    '''Opens a preview for user focusing, then takes series of pics
    for averaging and background subtraction'''
    with picamera.PiCamera() as camera:
        camera.resolution = (1664, 1232)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.2, 1.2)
        camera.framerate = 30
        camera.start_preview()
        pihat.brightness(1.0)
        pihat.clear()
        for y in range(16):
            for x in range(16):
                v = display[x, y]  # brightness depends on range
                if v == 0:
                    red = int(255)  # makes 0-1 range > 0-255 range
                    green = int(255)
                    blue = int(255)
                elif v == 1:
                    red = int(0)
                    green = int(0)
                    blue = int(0)
                elif v == 2:
                    red = int(0)
                    green = int(0)
                    blue = int(0)
                pihat.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
        pihat.rotation(180)
        pihat.show()  # show the pixels
        GPIO.output(VALVE, True)
        time.sleep(20)
        GPIO.output(VALVE, False)
        pihat.clear()
        pihat.off()
        camera.stop_preview()

def im_capture(bg):
    '''Cycles valve and captures an image to a numpy array'''
    #if bg == False:
    GPIO.output(VALVE, True)
    time.sleep(valve_time)
    GPIO.output(VALVE, False)
    time.sleep(valve_time)
    a = 255
    with picamera.PiCamera() as camera:
        pihat.brightness(1.0)
        pihat.clear()
        for y in range(16):
            for x in range(16):
                v = display[x, y]  # brightness depends on range
                if v == 0:
                    red = int(a)  # makes 0-1 range > 0-255 range
                    green = int(a)
                    blue = int(a)
                elif v == 1:
                    red = int(0)
                    green = int(0)
                    blue = int(0)
                elif v == 2:
                    red = int(0)
                    green = int(0)
                    blue = int(0)
                pihat.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
        pihat.rotation(180)
        pihat.show()  # show the pixels
        camera.resolution = (1664, 1232)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.2, 1.2)
        camera.framerate = 30
        output = np.empty((1232, 1664, 3), dtype=np.uint8)
        #camera.start_preview()
        time.sleep(2)
        camera.capture(output, 'rgb')
        time.sleep(1)
        #camera.stop_preview()
        pihat.clear()
        pihat.off()
    return output/255.


class Sample:
    '''Sample class to store information about each sample, which
    contains a series of device images and gets condensed into a single
    reading'''
    def __init__(self, sample_frequency, sample_volume, save_path,
                 save_images, save_images_path):
        self.start_time = datetime.datetime.now()
        self.frames = 0
        self.microbe_count = 0
        self.ecoli_count = 0
        self.yeast_count = 0
        self.sampled_vol = 0
        self.sample_volume = float(sample_volume)
        self.sample_time = sample_frequency
        self.save_path = save_path
        self.save = save_images
        self.save_im_path = save_images_path

    def add_pic(self):
        '''Captures and processes an image to the sample'''
        print("Adding pic...")
        new_pic = im_capture(False)
        #new_pic = new_pic - self.bg_avg
        self.frames += 1
        microbes, ecolis, yeasts = image_processing.process_image(new_pic, size=16)
        self.microbe_count += microbes
        self.ecoli_count += ecolis
        self.yeast_count += yeasts
        print("In this image:")
        print("Microbes: "+str(microbes)+", E coli: "+str(ecolis)+", Yeast: "+str(yeasts))
        print("Running total in this sample:")
        print("Microbes: "+str(self.microbe_count)+", E coli: "+str(self.ecoli_count)+", Yeast: "+str(self.yeast_count))
        if  os.path.isabs(self.save_path) == False:
            os.mkdirs(self.save_path)
        if self.save == True:
            print("Saving image...")
            t1 = time.time()
            imsave('%s%s.png' % (self.save_im_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")), new_pic)
            t2 = time.time()
            t_e = t2-t1
            print("Image saved in "+str(np.round(t_e,decimals=2))+" seconds.")

    def background(self):
        bg_array = np.empty((10, 1232, 1664, 3))
        for i in range(10):
            bg_im = im_capture(True)
            bg_im = bg_im/255.
            bg_array[i,:,:,:] = bg_im
            time.sleep(0.1)
            print("Calibrating background, image "+str(i+1)+" of 10...")
        self.bg_avg = np.mean(bg_array, axis=0)
        if self.save == True:
            t1 = time.time()
            imsave('%sbackground.png' % (self.save_im_path), self.bg_avg)
            t2 = time.time()
            t_e = t2-t1
            print("Background image saved in "+str(np.round(t_e,decimals=2))+" seconds.")


    def log(self):
        '''Writes .csv logfile with sample's results'''
        print("Writing log...")
        filename = '%s.csv' % self.save_path
        file_object = open(filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S,")
        concentration = self.microbe_count/self.sampled_vol
        file_object.write(now_string)
        file_object.write('Microbe count:,%d, ' % self.microbe_count +
                          'E coli count:,%d, ' % self.ecoli_count +
                          'Yeast count:,%d, ' % self.yeast_count +
                          'Sample Volume (uL):,%f,' % self.sampled_vol +
                          'Concentration (cells/uL):,%f,' % concentration + '\n')
        file_object.close()

    def temp_log(self):
        '''Writes .csv logfile with sample's results, for each image'''
        print("Recording Data to Temp File...")
        filename = '%s_tempfile.csv' % self.save_path
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
        #self.background()
        while (time.time() - loop_time) < self.sample_time and self.microbe_count < 1000 or self.sampled_vol < self.sample_volume:
            t1 = time.time()
            self.add_pic()
            t2 = time.time()
            pictime = t2-t1
            self.sampled_vol += 0.00896 #Sampled volume in uL
            self.temp_log()
            print('Image added in ' + str(np.round(pictime,decimals=2)) + ' seconds.')
        while (time.time() - loop_time) < self.sample_time:
            time.sleep(0.1)
        self.log()
        print('Logged result.')
