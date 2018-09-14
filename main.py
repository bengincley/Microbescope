from skimage.io import imread
from skimage.filters import threshold_otsu, gaussian, rank
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label
from skimage.morphology import erosion, disk, watershed
from skimage.feature import peak_local_max
from skimage.util import invert
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
from skimage.util import img_as_ubyte


def import_image(input_file):
    image = imread(input_file)
    return image


def binary_threshold(image):
    new_img = rgb2gray(image)
    gauss_img = gaussian(new_img, sigma=0.5) - gaussian(new_img, sigma=20)
    thresh = threshold_otsu(gauss_img)
    super_thresh = gauss_img < thresh
    gauss_img[super_thresh] = 0
    return gauss_img


def coordinates(binary):
    label_image = label(binary)
    image_label_overlay = label2rgb(label_image, image=binary)
    return image_label_overlay, label_image


input_file = 'Escherichia.coli/Escherichia.coli_0001.tif'
image = import_image(input_file)
image = rgb2gray(image)
image = invert(image)
gauss_image = binary_threshold(image)
#distance = ndi.distance_transform_edt(image)
local_maxi = peak_local_max(image, min_distance=9, threshold_abs=0.2, indices=False)
markers = ndi.label(local_maxi)[0]
overlay = label2rgb(markers, image=image)

plt.imshow(gauss_image, cmap=plt.cm.nipy_spectral, interpolation='nearest')
plt.show()
#print(len(local_maxi))