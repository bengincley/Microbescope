from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from MicrobeScope import image_processing
import datetime

# Pin Setup:
LED = 1 #Pin#
VALVE = 2
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)
GPIO.output(VALVE, False)

camera = PiCamera()
camera.resolution = (3200, 2400)
camera.awb_mode = 'off'
camera.awb_gains = (1, 1)


def ImCapture(self):
    GPIO.output(LED, True)
    time.sleep(1)
    GPIO.output(VALVE, True)
    time.sleep(Sample.valve_time)
    GPIO.output(VALVE, False)
    time.sleep(Sample.valve_time)
    camera.capture('/home/pi/Desktop/CameraTest/image%s.data' % i, 'rgb')

class Sample:
    def __init__(self):
        self.microbe_count = 0
        self.start_time = datetime.datetime.now()
        self.pics = []
        self.frames = 0

    def add_pic(self):
        pass

    def analyze_image(self):
        image_processing.

    def log(self, filename):
        file_object = open(filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S:%f")
        file_object.write(now_string)
        file_object.write(' - Result:%d ecoli, ' % self.microbe_count + '\n')
        file_object.close()