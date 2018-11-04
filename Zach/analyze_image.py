import datetime
import numpy as np
import pickle
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from skimage.feature import peak_local_max
from skimage.util import invert
import argparse
import time
import os, random


parser = argparse.ArgumentParser(description='Gather input parameters for MicrobeScope run')
parser.add_argument('-f', '--sample_frequency', help='number of samples per hour', type=int,
                    choices=range(1, 48), nargs='?', const=2)
args = parser.parse_args()
frequency = args.sample_frequency


def take_pic():
    directory = 'Neg_control/'
    filename = random.choice(os.listdir(directory))
    image = imread(directory+filename)
    return image


def pre_process(image):
    """ Preforms high-level pre-processing on image
    using difference of Gaussian filter and threshold
    """
    new_img = rgb2gray(image)
    new_img = invert(new_img)
    thresh = threshold_otsu(new_img)
    super_thresh = new_img < thresh
    new_img[super_thresh] = 0
    return new_img


def coordinates(image):
    """ Returns coordinates of local maxima in imag
    """
    local_maximums = peak_local_max(image, min_distance=5, threshold_abs=0.01, indices=True, exclude_border=30)
    return local_maximums


def extract_patches(image, coordinates, size):
    """ Returns image patches centered coordinates input into function
    """
    patch = []
    for i in range(len(coordinates)):
        patch.append(image[int((coordinates[i, 0] - size / 2)):int((coordinates[i, 0] + size / 2)),
                     int((coordinates[i, 1] - size / 2)):int((coordinates[i, 1] + size / 2))])
    patch = np.asarray(patch)
    patch = patch.reshape((len(patch), -1))
    return patch


def write_log(filename, result):
    file_object = open(filename, 'a')
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M")
    file_object.write(now_string)
    file_object.write(' - Result:%d ecoli, ' % result[0] + 'and %d staph' % result[1]+'\n')
    file_object.close()
    return


pkl_filename = 'pickle_model.pkl'
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)


def main():
    pic = take_pic()
    pre_pro = pre_process(pic)
    local_maxi = coordinates(pre_pro)
    patches = extract_patches(rgb2gray(pic), local_maxi, 30)
    results = pickle_model.predict_proba(patches)
    ecoli_array = results[:, 1] > 0.5
    staph_array = results[:, 2] > 0.5
    ecoli = np.count_nonzero(ecoli_array)
    staph = np.count_nonzero(staph_array)
    results = [ecoli, staph]
    write_log('test.txt', results)
    return ecoli


class Sample:
    def __init__(self):
        self.microbe_count = 0
        self.start_time = datetime.datetime.now()
        self.pics = []
        self.frames = 0

    def add_pic(self):
        pass

    def log(self, filename):
        file_object = open(filename, 'a')
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S:%f")
        file_object.write(now_string)
        file_object.write(' - Result:%d ecoli, ' % self.microbe_count + '\n')
        file_object.close()
#
#     def add_picture(self):
#         camera = PiCamera()
#         camera.resolution = (1024, 768)
#         gpio.digitalWrite(led_pin, gpio.HIGH)
#         time.sleep(0.1)
#         camera.capture()
#         return pic_array
#
# class Valve:
#     def __init__(self, pin):
#         self.open = False
#         self.pin = pin
#         self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_GPIO)
#         self.gpio.pinMode(self.pin, gpio.OUTPUT)
#
#     def open(self):


try:
    print('Press CTRL+C to quit')
    count = 0
    while True:
        loop_time = time.time()
        while (time.time()-loop_time) < 10 and count < 2000:
                count += main()
                print(count)
        while (time.time()-loop_time) < 10:
            time.sleep(0.1)
        count = 0
except KeyboardInterrupt:
    pass


