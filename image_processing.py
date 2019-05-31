"""Detailed Image processing and machine learning code
Written by Zach Flinkstrom and Ben Gincley"""
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
import pickle
from matplotlib import pyplot as plt

def object_detector(source_image, filter_size=16, threshold=0.12):
    """My favorite flavor of the function, yum"""
    k = np.array([[0.075, 0.124, 0.075], [0.124, 0.204, 0.124], [0.075, 0.124, 0.075]])
    smooth_image = ndi.convolve(source_image, k, mode='constant', cval=0.0)
    max_filter = ndi.maximum_filter(smooth_image, size=filter_size, mode='constant', cval=0)
    maxima = (smooth_image == max_filter)
    thresh = (max_filter > threshold)
    maxima[thresh == 0] = 0
    labeled, num_objects = ndi.label(maxima, structure=np.ones((3, 3)))
    slices = ndi.find_objects(labeled)
    xy = []
    for dy, dx in slices:
        x_center = (dx.start + dx.stop - 1) / 2
        y_center = (dy.start + dy.stop - 1) / 2
        xy.append((x_center, y_center))
    return np.asarray(xy)


def extract_patches(image, coordinates, size):
    """ Returns image patches centered coordinates input into function. Ensures patches are correct shape
    returns coordinates of patches"""
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
    modelfile = 'svm_model_v4.pkl'
    with open(modelfile, 'rb') as file:
        model = pickle.load(file)
    #print(patches)
    if len(patches)==0:
        print("patch is empty")
        results = np.array([0])
    else:
        patch = patches.reshape((len(patches), -1))
        results = model.predict_proba(patch)
    return np.asarray(results)


def process_image(image, size):
    '''Combines object detection, patch extraction, and classification'''
    bw_image = np.dot(image[..., :3], [0.299, 0.587, 0.114])  # modifies capture to grayscale for pre-processing
    objects = object_detector(bw_image)
    # print(len(objects))
    # plt.imshow(image)
    # plt.plot(objects[:,0], objects[:,1], 'ro', alpha=0.35)
    # plt.show()
    patches, coordinates = extract_patches(image, objects, size)
    predictions = sklearn_predict(patches)
    #print("predictions: " +str(predictions))
    if predictions.all() == 0:
        number_microbes = 0
        number_ecoli = 0
        number_yeast = 0
    else:
        number_microbes = np.sum(predictions[:, 1] > 0.6) + np.sum(predictions[:, 2] > 0.6) # returns number of bacteria and yeast
        number_ecoli = np.sum(predictions[:, 1] > 0.6)
        number_yeast = np.sum(predictions[:, 2] > 0.6)
    #print(number_microbes)
    return number_microbes, number_ecoli, number_yeast

## Quality Control:
# image = np.array(Image.open("top_right.png").convert('RGB'))/255
# n = process_image(image, 16)
# print(n)
