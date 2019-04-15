'''Saves image patches to file based on json coordinates output from labelme. Modify file names and label
to save patches for bacteria, debris, or yeast.
Written by Zach Flinkstrom'''
import json
import numpy as np
import scipy.misc
from skimage.io import imread

# Load json of manually annotated cells from Labelme
file = 'Test_12_7_18/10e0/10e0_0.json'
with open(file) as f:
    data = json.load(f)
# Store coordinates of annotated cells vs annotated background
microbes = []
not_microbes = []
for i in data['shapes']:
    if i['label'] == 'debris':
        x = [x[0] for x in i['points']]
        y = [y[1] for y in i['points']]
        coordinate = [int(np.mean(x)), int(np.mean(y))]
        microbes.append(coordinate)


def extract_patches(image, coordinates, size):
    """ Saves image patches centered on input coordinates"""
    patch = []
    for i in range(len(coordinates)):
        new_patch = image[int((coordinates[i][1] - size / 2)):int((coordinates[i][1] + size / 2)),
                          int((coordinates[i][0] - size / 2)):int((coordinates[i][0] + size / 2))]
        print(new_patch.shape)
        if new_patch.shape == (16, 16, 4):
            num = i
            scipy.misc.imsave('data/final_train/debris/debris%d.png'%num,new_patch)
            print('saved')
    return patch


image = imread('Test_12_7_18/10e0/10e0_0.png')
extract_patches(image, microbes, 16)