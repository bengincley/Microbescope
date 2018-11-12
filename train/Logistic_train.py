import os
from skimage.io import imread
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from sklearn import svm, metrics
from sklearn.linear_model import LogisticRegression
import pickle
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
x_train = x_train.astype('float64')
x_test = x_test.astype('float64')
num_train = len(x_train)
num_test = len(x_test)
x_train = x_train.reshape((num_train, -1))
x_test1 = x_test.reshape((num_test, -1))
# Create a classifier: a support vector classifier
classifier = LogisticRegression()

# We learn the digits on the first half of the digits
classifier.fit(x_train, y_train)

# # Now predict the value of the digit on the second half:
expected = y_test
predicted = classifier.predict(x_test1)

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

pkl_filename = "Logistic_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)
plt.close()
co1 = classifier.coef_[0]
co1 = co1.reshape(30,30)
co2 = classifier.coef_[1]
co2 = co2.reshape(30,30)
co3 = classifier.coef_[2]
co3 = co3.reshape(30,30)
fig, axs = plt.subplots(1,3)
axs[0].imshow(co1)
axs[1].imshow(co2)
axs[2].imshow(co3)
plt.show()
