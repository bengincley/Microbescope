import time
import numpy as np
import colorsys
import picamera
from time import sleep
import RPi.GPIO as GPIO

try:
    import unicornhathd as unicornhathd
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicornhathd

VALVE = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(VALVE, False)

camera = picamera.PiCamera()
camera.resolution = (1640, 1232)
camera.framerate = 30
camera.awb_mode = 'off'
camera.awb_gains = (1.2,1.2)
camera.start_preview()

print("""Unicorn HAT HD: Press Ctrl+C to exit!""")
x = np.array(range(15))
y = np.array(range(15))
unicornhathd.brightness(1.0)


ring3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
         [1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 1, 1, 1],
         [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1],
         [1, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1],
         [1, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1],
         [1, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1],
         [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1],
         [1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
ring3 = np.array(ring3)
turtle = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 3, 2, 0, 0],
         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0],
         [0, 0, 0, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0],
         [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
turtle = np.array(turtle)

unicornhathd.clear()
a = 255
for y in range(16):
    for x in range(16):
        v = ring3[x, y]  # brightness depends on range
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
        elif v == 3:
            red = int(0)
            green = int(0)
            blue = int(0)
        unicornhathd.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
unicornhathd.rotation((90))
unicornhathd.show()  # show the pixels
sleep(1)
n = 60
GPIO.output(VALVE, True)
print("Valve open for "+str(n)+" seconds...")
sleep(n)
GPIO.output(VALVE, False)
sleep(1)
print("valve closed")
sleep(1)
for y in range(16):
    for x in range(16):
        v = turtle[x, y]  # brightness depends on range
        if v == 0:
            red = int(0)  # makes 0-1 range > 0-255 range
            green = int(0)
            blue = int(0)
        elif v == 1:
            red = int(0)
            green = int(a)
            blue = int(a/2)
        elif v == 2:
            red = int(a/2)
            green = int(a)
            blue = int(0)
        elif v == 3:
            red = int(a)
            green = int(a)
            blue = int(a)
        unicornhathd.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
unicornhathd.rotation(180)
unicornhathd.show()  # show the pixels
print("Clean Turtle :)")
sleep(2)
unicornhathd.off()
camera.stop_preview()
