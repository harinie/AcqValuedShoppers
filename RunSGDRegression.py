#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
# Read train and test data and run SVM

import numpy as np
import pylab as pl

from gen_submission import generate_submission
from sklearn.cross_validation import ShuffleSplit, StratifiedShuffleSplit
from sklearn.linear_model import SGDRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn import datasets
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

loc_testHist = "//home//harini//Kaggle_data//shop//testHistory.csv"
loc_preds = "testsubmission_huber_07042014.csv"
loc_submission = "submission_huber_07042014.csv"
loc_train = "//home//harini//Kaggle_data//shop//train_07042014.csv"
loc_test = "//home//harini//Kaggle_data//shop//test_07042014.csv"
#loc_train = "//home//harini//Kaggle_data//shop//train.csv"
#loc_test = "//home//harini//Kaggle_data//shop//test.csv"

# Extract data into X and y
def extract_data(filename):
	data = np.genfromtxt(filename, delimiter = ',') 
	[N,m] = data.shape
	data = data[1:N,0:m-1] # remove header and last column
	[N,m] = data.shape
	print(data.shape)

	#find label column
	header=[]
	try:
		fp = open(filename)
		line = fp.readline()
		header = line.strip().split(",")

	finally:
		fp.close()

	for e,x in enumerate(header):
		if (x == "label"):
			label_col = e
		if (x == "category"):
			cat_col = e
		if (x == "id"):
			id_col = e

	y = data[:,[label_col]]
	category = data[:, [cat_col]]
	ids = data[:,[id_col]]
	X = np.delete(data,[id_col,label_col,cat_col],1)
	del data	

	print(X.shape)
	print(y.shape)
	return (X,y,category,header,ids)
	
	
X, y, category, header, ids = extract_data(loc_train)

[N,m] = X.shape
corr_X_y = np.corrcoef(np.concatenate((X,y),axis=1),rowvar=0)
#plt.pcolor(corr_X_y, vmin=0, vmax=1)
#plt.colorbar()		
#plt.show()

count=0
for e,x in enumerate(header):
	if (x == "label" or x == "id" or x == "category" or x == ""):
		print(e,x,"nan")
		count += 1
		continue
	print(e,x,corr_X_y[m,e-count])
		
X = StandardScaler().fit_transform(X)
y = np.ravel(y)
loss="huber"
epsilon=0.1

#l2 svm
cv=StratifiedShuffleSplit(category, n_iter=10, test_size=0.5, train_size=None, indices=True, random_state=None)
tuned_parameters = [{'alpha': [0.001,0.005,0.01,0.05,0.1,0.5,1,5,10,50,100,500,1000]}]
clf_svm = SGDRegressor(loss=loss, penalty='l2',shuffle=True)
clf = GridSearchCV(clf_svm, tuned_parameters, scoring='roc_auc', cv=cv,refit=True)
clf.fit(X, y)

for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"% (mean_score, scores.std() / 2, params))

  
# final training and testing
clf.best_estimator_.fit(X,y)
coef_svm = clf.best_estimator_.coef_.ravel()
	
count=0
outline=""
out_coeffs = open("coeffs_full_huber_05172014_l2.csv", "w+")
for e,x in enumerate(header):
	if (x == "label" or x == "id" or x == "category" or x ==""):
		print(e,x,"nan")
		count += 1
		continue
	print(e,x,coef_svm[e-count])
	outline += x+","+str(coef_svm[e-count])+"\n"
out_coeffs.write( outline )
out_coeffs.close()	
	
y_train = clf.best_estimator_.decision_function(X)
plt.scatter(y,y_train)
#plt.ylim(0,1)
plt.show()

submission = np.array([ids,y_train])
submission= np.transpose(submission)

np.savetxt("temp.csv", submission, fmt="%d,%1.6f")


X_test, y_test, category_test, header_test, id_test = extract_data(loc_test)
X_test = StandardScaler().fit_transform(X_test)

y_test = clf.best_estimator_.decision_function(X_test)

plt.hist(y_test,bins=np.arange(-1,1,0.1))
plt.show()

submission = np.array([id_test,y_test])
submission= np.transpose(submission)

np.savetxt(loc_preds, submission, fmt="%d,%1.6f")

generate_submission(loc_preds, loc_testHist, loc_submission)

