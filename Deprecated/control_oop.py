from picamera import PiCamera
import time
import RPi.GPIO as GPIO

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

class Sample:
    n_im_req = 10
    valve_time = 0.5

    def __init__(self):
        self.time = time.asctime()
        self.cell_count = 0
        self.completed_sample = 0 # Have looping check if this = 1, stop sample; change to = 1 w/ stat. signif. -- sum(cell_count)>385

    def ImCapture(self,i):
        GPIO.output(LED, True)
        camera.start_preview()
        time.sleep(1)
        GPIO.output(VALVE, True)
        time.sleep(Sample.valve_time)
        GPIO.output(VALVE, False)
        time.sleep(Sample.valve_time)
        camera.capture('/home/pi/Desktop/CameraTest/image%s.data' % i, 'rgb')



