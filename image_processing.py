"""Detailed Image processing and machine learning code
Written by Zach Flinkstrom and Ben Gincley"""
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
import pickle


def object_detector(image, filter_size=15, threshold=-0.02):
    """returns coordinates of local minima after gaussian filtering"""
    k = np.array([[0.075, 0.124, 0.075], [0.124, 0.204, 0.124], [0.075, 0.124, 0.075]])
    image = ndi.convolve(image, k, mode='constant', cval=0.0)
    min_filter = ndi.minimum_filter(image, size=filter_size, mode='constant', cval=0)
    minima = (image == min_filter)
    thresh = (min_filter < threshold)
    minima[thresh == 0] = 0
    labeled, num_objects = ndi.label(minima, structure=np.ones((3,3)))
    slices = ndi.find_objects(labeled)  
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
        if square.shape == (size, size, 3):
            patch.append(square)
            xy.append(coordinates[i])
    return np.asarray(patch), np.asarray(xy)


def sklearn_predict(patches):
    '''Predicts class of patch 0 = debris, 1 = bacteria, 2 = yeast
    modelfile can be changed to svm.pkl for svm usage'''
    modelfile = 'logistic_model_v3.pkl'
    with open(modelfile, 'rb') as file:
        model = pickle.load(file)
    patch = patches.reshape((len(patches), -1))
    results = model.predict_proba(patch)
    return np.asarray(results)


def process_image(image, size):
    '''Combines object detection, patch extraction, and classification'''
    bw_image = np.dot(image[..., :3], [0.299, 0.587, 0.114])  # modifies capture to grayscale for pre-processing
    objects = object_detector(bw_image)
    patches, coordinates = extract_patches(image, objects, size)
    predictions = sklearn_predict(patches)
    number_microbes = np.sum(predictions[:, 1] > 0.6) + np.sum(predictions[:, 2] > 0.6) # returns number of bacteria and yeast
    return number_microbes


