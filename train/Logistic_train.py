'''Code to train Logistic Model'''
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, metrics
from sklearn.linear_model import LogisticRegression
import pickle
from PIL import Image

'''Import training images and labels'''
ecoli_folder = 'data/final_train/ecoli'
yeast_folder = 'data/final_train/yeast'
debris_folder = 'data/final_train/debris'
images = []
labels = []
for filename in os.listdir(debris_folder):
    img = np.array(Image.open(os.path.join(debris_folder, filename)).convert('RGB'))
    img = img/255.
    if img is not None:
        images.append(img)
        labels.append(0)
for filename in os.listdir(ecoli_folder):
    img = np.array(Image.open(os.path.join(ecoli_folder, filename)).convert('RGB'))
    img = img/255.
    if img is not None:
        images.append(img)
        labels.append(1)
for filename in os.listdir(yeast_folder):
    img = np.array(Image.open(os.path.join(yeast_folder, filename)).convert('RGB'))
    img = img/255.
    if img is not None:
        images.append(img)
        labels.append(2)

'''Set up image and labels for training and testing'''
labels = np.asarray(labels)
images = np.asarray(images)
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.33)
x_train = x_train.astype('float64')
x_test = x_test.astype('float64')
num_train = len(x_train)
num_test = len(x_test)
x_train = x_train.reshape((num_train, -1))
x_test1 = x_test.reshape((num_test, -1))
'''Define Logistic classifier and train'''
classifier = LogisticRegression()
classifier.fit(x_train, y_train)
expected = y_test
predicted = classifier.predict(x_test1)

'''Print and plot results of model testing'''
print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
images_and_predictions = list(zip(x_test, predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    plt.subplot(4, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
plt.show()
'''Save model to file'''
pkl_filename = "logistic_model_v3.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)
'''Plot the learned logistic kernels for image patches'''
plt.close()
co1 = classifier.coef_[0]
co1 = co1.reshape(16, 16, 3)
co2 = classifier.coef_[1]
co2 = co2.reshape(16, 16, 3)
co3 = classifier.coef_[2]
co3 = co3.reshape(16, 16, 3)
fig, axs = plt.subplots(1, 3)
axs[0].imshow(co1)
axs[1].imshow(co2)
axs[2].imshow(co3)
plt.show()
