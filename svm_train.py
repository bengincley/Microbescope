'''Code to train SVM model'''
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, metrics
import pickle
from PIL import Image

'''Import training images and labels'''
ecoli_folder = '4-10/data/ecoli'
yeast_folder = '4-10/data/yeast'
debris_folder = '4-10/data/debris'
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
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.2)
x_train = x_train.astype('float64')
x_test = x_test.astype('float64')
num_train = len(x_train)
num_test = len(x_test)
x_train = x_train.reshape((num_train, -1))
x_test1 = x_test.reshape((num_test, -1))

'''Define SVM classifier parameters'''
classifier = svm.SVC(C=100., gamma=0.1, probability=True, decision_function_shape='ovr')
classifier.fit(x_train, y_train)  # fit the SVM with training data
expected = y_test
predicted = classifier.predict(x_test1)  # Test the trained model on testing data

'''Print and plot results of model testing'''
print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
images_and_predictions = list(zip(x_test, predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:8]):
    plt.subplot(4, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
plt.show()

'''Save model to pickle file'''
pkl_filename = "svm_model_v4.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)
