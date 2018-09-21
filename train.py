from __future__ import print_function
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
import json
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

file = 'Escherichia.coli/Escherichia.coli_0001.json'
with open(file) as f:
    data = json.load(f)

microbes = []
not_microbes = []
for i in data['shapes']:
    if i['label'] == 'a':
        microbes.append(i['points'][0])
    else:
        not_microbes.append(i['points'][0])


def extract_patches(image, coordinates, size):
    patch = []
    for i in range(len(coordinates)):
        new_patch = image[int((coordinates[i][1] - size / 2)):int((coordinates[i][1] + size / 2)),
                          int((coordinates[i][0] - size / 2)):int((coordinates[i][0] + size / 2))]
        if new_patch.shape == (30, 30, 3):
            patch.append(new_patch)
    return patch


image = imread('Escherichia.coli/'+data['imagePath'])
microbes_patches = extract_patches(image, microbes, 30)
not_microbes_patches = extract_patches(image, not_microbes, 30)
X = np.concatenate((microbes_patches, not_microbes_patches))
y = np.concatenate((np.ones(len(microbes_patches), dtype=int), np.zeros(len(not_microbes_patches), dtype=int)))
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#Keras CNN Example from treszkai
#https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
batch_size = 128
num_classes = 2
epochs = 10

# input image dimensions
img_x, img_y = 30, 30


# reshape the data into a 4D tensor - (sample_number, x_img_size, y_img_size, num_channels)
# because the MNIST is greyscale, we only have a single channel - RGB colour images would have 3
x_train = x_train.reshape(x_train.shape[0], img_x, img_y, 3)
x_test = x_test.reshape(x_test.shape[0], img_x, img_y, 3)
input_shape = (img_x, img_y, 3)

# convert the data to the right type
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices - this is for use in the
# categorical_crossentropy loss below
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
                 activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(64, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(1000, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])


class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))

history = AccuracyHistory()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test),
          callbacks=[history])
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
plt.plot(range(1, 11), history.acc)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.show()

from main import patch as auto_patches
auto_patches = np.asarray(auto_patches)
auto_patches = auto_patches.reshape(auto_patches.shape[0], img_x, img_y, 3)
auto_patches = auto_patches.astype('float32')
auto_patches /= 255

results = model.predict(auto_patches)
