import numpy as np
from PIL import Image
import scipy.ndimage as ndi
import pickle


def import_image(input_file):
    """Imports image files as arrays and inverts them to make cells high pixel values
    """
    image = np.array(Image.open(input_file).convert('L'))
    image = np.invert(image)
    return image


def object_detector(image, filter_size=10, threshold=0.2):
    """My favorite flavor of the function, yum"""
    k = np.array([[0.075, 0.124, 0.075], [0.124, 0.204, 0.124], [0.075, 0.124, 0.075]])
    orig_image = ndi.convolve(image, k, mode='constant', cval=0.0)
    max_filter = ndi.maximum_filter(orig_image, size=filter_size, mode='constant', cval=0)
    maxima = (orig_image == max_filter)
    thresh = (max_filter > threshold)
    maxima[thresh == 0] = 0
    labeled, num_objects = ndi.label(maxima, structure=np.ones((3, 3)))
    slices = ndi.find_objects(labeled)  # 15ms
    xy = []
    for dy, dx in slices:
        x_center = (dx.start + dx.stop - 1) / 2
        y_center = (dy.start + dy.stop - 1) / 2
        xy.append((x_center, y_center))
    return np.asarray(xy)


def extract_patches(image, coordinates, size):
    """ Returns image patches centered coordinates input into function. Ensures patches are correct shape
    returns coordinates of patches
    """
    patch = []
    xy = []
    for i in range(len(coordinates)):
        square = image[int((coordinates[i, 1] - size / 2)):int((coordinates[i, 1] + size / 2)),
                       int((coordinates[i, 0] - size / 2)):int((coordinates[i, 0] + size / 2))]
        if square.shape == (size, size):
            patch.append(square)
            xy.append(coordinates[i])
    return np.asarray(patch), np.asarray(xy)


def sklearn_predict(patches):
    modelfile = 'Logistic_model.pkl'
    with open(modelfile, 'rb') as file:
        model = pickle.load(file)
    patch = patches.reshape((len(patches), -1))
    results = model.predict_proba(patch)
    return np.asarray(results)


def process_image(image, size):
    objects = object_detector(image)
    patches, coordinates = extract_patches(image, objects, size)
    predictions = sklearn_predict(patches)
    number_microbes = len(predictions[:, 1]>0.5)
    return number_microbes


