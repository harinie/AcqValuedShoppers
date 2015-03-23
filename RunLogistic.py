#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
# Read train and test data and run Logistic regression

import numpy as np
import pylab as pl

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

loc_train = "//home//harini//Kaggle_data//shop//train.csv"
loc_test = "//home//harini//Kaggle_data//shop//test.csv"

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
	
def generate_cv_indices(category):
	N = len(category)
	u, indices = np.unique(category, return_inverse=True)
	#print(u)
	train_inds = np.repeat([False],N)
	test_inds = np.repeat([False],N)
	start = 0
	for i in range(0,len(u)):
		i_inds = np.where(indices == i)
		#print(i_inds)
		N_i = len(i_inds[0])
		N_i_train = np.floor(N_i/2)
		train_inds[i_inds[0][0:N_i_train]] = True
		test_inds[i_inds[0][N_i_train+1:N_i]] = True
	return np.concatenate((train_inds,test_inds),axis=1)
	
	
def logistic_cross_validate_category(X,y,category,C,penalty):
	
	clf_LR_1 = LogisticRegression(C=C, penalty=penalty, tol=0.01)
	clf_LR_2 = LogisticRegression(C=C, penalty=penalty, tol=0.01)
	
	cv_indices = generate_cv_indices(category)
	train_ids = cv_indices[0:N]
	test_ids = cv_indices[N:2*N]
	
	clf_LR_1.fit(X[train_ids,:], y[train_ids])
	clf_LR_2.fit(X[test_ids,:], y[test_ids])
	
	score = np.zeros(2)
	score[0] = clf_LR_1.score(X[test_ids,:], y[test_ids])
	score[1] = clf_LR_2.score(X[train_ids,:], y[train_ids])
	mean_score = np.mean(score)
	
	y_1 = clf_LR_1.predict_proba(X[test_ids,:])
	y_2 = clf_LR_2.predict_proba(X[train_ids,:])
	
	u, indices = np.unique(category, return_inverse=True)
	auc = np.zeros((2,len(u)))
	for i in range(0,len(u)):
		
		i_inds = indices == i
		
		fpr, tpr, thresholds = metrics.roc_curve(y[test_ids & i_inds], y_1[i_inds[test_ids],1], pos_label=1)
		auc[0,i] = metrics.auc(fpr, tpr)

		fpr, tpr, thresholds = metrics.roc_curve(y[train_ids & i_inds], y_2[i_inds[train_ids],1], pos_label=1)
		auc[1,i] = metrics.auc(fpr, tpr)	
	
		mean_auc = np.mean(auc,axis=0)
	
	return mean_auc
	
def logistic_cross_validate(X,y,category,C,penalty):
	
	clf_LR_1 = LogisticRegression(C=C, penalty=penalty, tol=0.01)
	clf_LR_2 = LogisticRegression(C=C, penalty=penalty, tol=0.01)
	
	N = len(category)
	half_data= np.floor(N/2)
	cv_indices_1= np.repeat([False],N)
	cv_indices_2= np.repeat([False],N)
	cv_indices_1[0:half_data] =True
	cv_indices_2[half_data:N] =True
	cv_indices= np.concatenate((cv_indices_1,cv_indices_2),axis=1)
	
	train_ids = cv_indices[0:N]
	test_ids = cv_indices[N:2*N]
	
	clf_LR_1.fit(X[train_ids,:], y[train_ids])
	clf_LR_2.fit(X[test_ids,:], y[test_ids])
	
	score = np.zeros(2)
	score[0] = clf_LR_1.score(X[test_ids,:], y[test_ids])
	score[1] = clf_LR_2.score(X[train_ids,:], y[train_ids])
	mean_score = np.mean(score)
	
	y_1 = clf_LR_1.predict_proba(X[test_ids,:])
	y_2 = clf_LR_2.predict_proba(X[train_ids,:])
	
	auc = np.zeros(2)
	fpr, tpr, thresholds = metrics.roc_curve(y[test_ids], y_1[:,1], pos_label=1)
	auc[0] = metrics.auc(fpr, tpr)

	fpr, tpr, thresholds = metrics.roc_curve(y[train_ids], y_2[:,1], pos_label=1)
	auc[1] = metrics.auc(fpr, tpr)	
	
	mean_auc = np.mean(auc,axis=0)
	
	return mean_auc
    
X, y, category, header, ids = extract_data(loc_train)
[N,m] = X.shape
corr_X_y = np.corrcoef(np.concatenate((X,y),axis=1),rowvar=0)
plt.pcolor(corr_X_y, vmin=0, vmax=1)
plt.colorbar()		
#plt.show()

count=0
for e,x in enumerate(header):
	if (x == "label" or x == "id" or x == "category" or x==""):
		print(e,x,"nan")
		count += 1
		continue
	print(e,x,corr_X_y[m,e-count])
		
X = StandardScaler().fit_transform(X)
y = np.ravel(y)


# l1 logistic
for i, C in enumerate(10. ** np.arange(-4, 4)):
    # turn down tolerance for short training time
   cv_auc =logistic_cross_validate(X,y,category,C,'l1')
   print("The cv auc for l1 C=%1.4f is %1.4f"% (C,np.mean(cv_auc)))
   print(cv_auc)
   
# l2 logistic
for i, C in enumerate(10. ** np.arange(-4, 4)):
    # turn down tolerance for short training time
   cv_auc =logistic_cross_validate(X,y,category,C,'l2')
   print("The cv auc for l2 C=%1.4f is %1.4f"% (C,np.mean(cv_auc)))
   print(cv_auc)
   
   
# final training and testing
clf_LR = LogisticRegression(C=0.0001, penalty='l2', tol=0.01)
clf_LR.fit(X,y)
coef_LR = clf_LR.coef_.ravel()
	
count=0
outline=""
out_coeffs = open("coeffs_04272014.csv", "w+")
for e,x in enumerate(header):
	if (x == "label" or x == "id" or x == "category" or x ==""):
		print(e,x,"nan")
		count += 1
		continue
	print(e,x,coef_LR[e-count])
	outline += x+","+str(coef_LR[e-count])+"\n"
out_coeffs.write( outline )
out_coeffs.close()	
	


y_train = clf_LR.predict_proba(X)

submission = np.array([ids,y_train[:,1]])
submission= np.transpose(submission)

np.savetxt("temp.csv", submission, fmt="%d,%1.6f")


X_test, y_test, category_test, header_test, id_test = extract_data(loc_test)
X_test = StandardScaler().fit_transform(X_test)
y_test = clf_LR.predict_proba(X_test)


submission_file="criteo_submission_05162014.csv"
outfile = open(submission_file, "w+")
outfile.write( "Id,Predicted\n" )
for e,val in enumerate(id_test):
	outfile.write(val+","+y_test[e,1]+"\n")
outfile.close()

