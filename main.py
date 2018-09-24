import numpy as np
import keras
from keras.models import model_from_json
from skimage.io import imread
from skimage.filters import threshold_otsu, gaussian
from skimage.color import rgb2gray
from skimage.feature import peak_local_max
from skimage.util import invert


def import_image(input_file):
    image = imread(input_file)
    return image


def pre_process(image):
    """ Preforms high-level pre-processing on image
    using difference of Gaussian filter and threshold
    """
    new_img = rgb2gray(image)
    new_img = invert(new_img)
    gauss_img = gaussian(new_img, sigma=0.5) - gaussian(new_img, sigma=20)
    thresh = threshold_otsu(gauss_img)
    super_thresh = gauss_img < thresh
    gauss_img[super_thresh] = 0
    return gauss_img


def coordinates(image):
    """ Returns coordinates of local maxima in imag
    """
    local_maximums = peak_local_max(image, min_distance=9, threshold_abs=0.2, indices=True, exclude_border=30)
    return local_maximums


def extract_patches(image, coordinates, size):
    """ Returns image patches centered coordinates input into function
    """
    patch = []
    for i in range(len(coordinates)):
        patch.append(image[int((coordinates[i, 0] - size / 2)):int((coordinates[i, 0] + size / 2)),
                     int((coordinates[i, 1] - size / 2)):int((coordinates[i, 1] + size / 2))])
    return patch


# Import test image and process into patches
input_img = 'Escherichia.coli/Escherichia.coli_0002.tif'
orig_image = import_image(input_img)
gauss_image = pre_process(orig_image)
local_maxi = coordinates(gauss_image)
patch = extract_patches(orig_image, local_maxi, 30)
# Reformat patches into form acceptable to model
img_x, img_y = 30, 30
patch = np.asarray(patch)
patch = patch.reshape(patch.shape[0], img_x, img_y, 3)
patch = patch.astype('float32')
patch /= 255
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
loaded_model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
# Test trained model using automatically extracted local-max patches
results = loaded_model.predict(patch)
print(results[0])
