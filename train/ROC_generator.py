"""Script for generating ROC curves with 6-fold cross validation
can generate curve for svm or logistic depending on which classifier line is commented out
Code modified from Sklearn Example:
https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
#sphx-glr-auto-examples-model-selection-plot-roc-crossval-py"""
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, metrics
from sklearn.linear_model import LogisticRegression
import pickle
from PIL import Image
from scipy import interp
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold

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
        labels.append(1)

labels = np.asarray(labels)
images = np.asarray(images)
# Create a classifier: a support vector classifier or Logistic if you comment out
classifier = svm.SVC(C=100., gamma=0.1, probability=True, decision_function_shape='ovr')
#classifier = LogisticRegression()


#############################################################################
X = images
X = X.reshape((len(X), -1))
y = labels
X, y = X[y != 2], y[y != 2]
n_samples, n_features = X.shape

# #############################################################################
# Classification and ROC analysis

# Run classifier with cross-validation and plot ROC curves
cv = StratifiedKFold(n_splits=6)

tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)

i = 0
for train, test in cv.split(X, y):
    probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=1, alpha=0.3,
             label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

    i += 1
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
         label='Chance', alpha=.8)

mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
plt.plot(mean_fpr, mean_tpr, color='b',
         label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                 label=r'$\pm$ 1 std. dev.')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Logistic Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

