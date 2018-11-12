import os
from skimage.io import imread
from sklearn.model_selection import train_test_split
from keras.optimizers import SGD
import keras
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.callbacks import TensorBoard
from time import time
from sklearn.preprocessing import LabelEncoder
from PIL import Image

folder = 'data/sn_train'
images = []
labels = []
for filename in os.listdir(folder):
    img = np.array(Image.open(os.path.join(folder, filename)).convert('L'))
    img = np.invert(img)
    img = img/255.
    if img is not None:
        images.append(img)
    if filename[0] == 'e':
        labels.append(1)
    elif filename[0] == 'b':
        labels.append(0)
    else:
        labels.append(2)


labels = np.asarray(labels)
images = np.asarray(images)
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.33)

batch_size = 32
num_classes = 3
epochs = 50

# input image dimensions
img_x, img_y = 30, 30

# reshape the data into a 4D tensor - (sample_number, x_img_size, y_img_size, num_channels)
# because the MNIST is greyscale, we only have a single channel - RGB colour images would have 3
x_train = x_train.reshape(x_train.shape[0], img_x, img_y, 1)
x_test = x_test.reshape(x_test.shape[0], img_x, img_y, 1)
input_shape = (img_x, img_y, 1)

# convert the data to the right type
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# convert class vectors to binary class matrices - this is for use in the
# categorical_crossentropy loss below
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

sgd = SGD(lr=0.005, decay=0.0002, momentum=0.9, nesterov=True)
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1),
                 activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(25, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=sgd,
              metrics=['accuracy'])


class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))


history = AccuracyHistory()
tensorboard = TensorBoard(log_dir="logs/simplenet7withbackground/{}".format(time()))
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test),
          callbacks=[tensorboard])

score = model.evaluate(x_test, y_test, verbose=1)

# serialize model to JSON
model_json = model.to_json()
with open("simplenet7withbackground.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("simplenet7withbackground.h5")
print("Saved model to disk")