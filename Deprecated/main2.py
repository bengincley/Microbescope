# Main initial image pre-processing script
# Written by Zachary Flinkstrom and Benjamin Gincley, Sept. 2018

# Imports
from skimage import feature, morphology
from skimage.io import imread
from skimage.filters import threshold_otsu, gaussian, sobel, rank
from skimage.color import rgb2gray, label2rgb
from skimage.measure import regionprops, label
from skimage.morphology import label, erosion, disk, watershed
from skimage.feature import peak_local_max
from skimage.util import invert
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import ndimage as ndi
from skimage.util import img_as_ubyte

# Import single image file
def import_image(input_file):
    image = imread(input_file)
    return image

# Perform difference of gaussian filtering, set background to 0
def binary_threshold(image):
    new_img = rgb2gray(image)
    gauss_img = gaussian(new_img, sigma=0.5) - gaussian(new_img, sigma=20)
    thresh = threshold_otsu(gauss_img)
    sup_thresh = gauss_img > thresh
    gauss_img[sup_thresh] = 1
    return gauss_img

# Identifies coordinates
def coordinates(binary):
    binary_img = binary > threshold_otsu(binary)
    label_image = label(binary_img)
    image_label_overlay = label2rgb(label_image, image=binary)
    return image_label_overlay, label_image


# Main pipeline
input_file = 'input_image.tif'
image = import_image(input_file)
image = rgb2gray(image)
image = invert(image)
gauss_image = binary_threshold(image)
image_label_overlay, label_image = coordinates(gauss_image)
#rprops = regionprops(image_label_overlay)
#labeled = label2rgb(label_image, image=input_file, alpha=0.7, bg_label=0, bg_color=(0,0,0), image_alpha=1, kind = 'overlay')
#distance = ndi.distance_transform_edt(image)
local_maxi = peak_local_max(image, min_distance=9, threshold_abs=0.2, indices=False)
#markers = ndi.label(local_maxi)[0]
#overlay = label2rgb(markers, image=image)
edges = feature.canny(gauss_image, sigma=1)
fill_edges = ndi.binary_fill_holes(edges)
removed_small = morphology.remove_small_objects(fill_edges, 20)
elevation_map = sobel(gauss_image)
markers = np.zeros_like(gauss_image)
markers[gauss_image<.01] = 1
markers[gauss_image>.25] = 2
segmentation = morphology.watershed(elevation_map, markers)

segmentation = ndi.binary_fill_holes(segmentation - 1)
labeled_cells, _ = ndi.label(segmentation)
image_label_overlay = label2rgb(labeled_cells, image=gauss_image)

# Plotting
fig, ax = plt.subplots(1, 2, figsize=(8, 6), sharey=True)
ax[0].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax[0].contour(segmentation, [0.5], linewidths=1.2, colors='r')
ax[1].imshow(gauss_image, interpolation='nearest')
#plt.imshow(gauss_image, cmap=plt.cm.nipy_spectral, interpolation='nearest')
plt.show()
#print(len(local_maxi))