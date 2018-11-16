from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from MicrobeScope import image_processing
import datetime
import numpy as np

# Pin Setup:
LED = 1 #Pin#
VALVE = 2
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(LED, False)
GPIO.output(VALVE, False)


def im_capture():
    GPIO.output(LED, True)
    GPIO.output(VALVE, True)
    time.sleep(Sample.valve_time)
    GPIO.output(VALVE, False)
    time.sleep(Sample.valve_time)
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.awb_mode = 'off'
        camera.awb_gains = (1, 1)
        output = np.empty((2464, 3296, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        output = output[:, :3280, :] # strip off uninitialized pixels
    GPIO.output(LED, False)
    return output


class Sample(sample_frequency, logfile):
    valve_time = 0.5

    def __init__(self, sample_frequency, logfile):
        self.microbe_count = 0
        self.start_time = datetime.datetime.now()
        self.pics = []
        self.frames = 0
        self.sample_frequency = sample_frequency
        self.logfile = logfile

    def add_pic(self):
        new_pic = im_capture()
        self.pics.append(new_pic)
        self.frames += 1
        self.microbe_count += image_processing(new_pic)

    def log(self):
        filename = self.logfile
        file_object = open('%s.txt' % filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S:%f")
        file_object.write(now_string)
        file_object.write(' - Result:%d microbes, ' % self.microbe_count + '\n')
        file_object.close()

    def sample_run(self):
        loop_time = time.time()
        while (time.time() - loop_time) < self.sample_time and self.microbe_count < 400:
            self.add_pic()
        while (time.time() - loop_time) < self.sample_time:
            time.sleep(0.1)
        self.log()
