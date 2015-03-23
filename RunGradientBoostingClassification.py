#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
# Read train and test data and run SVM

import numpy as np
import pylab as pl

from sklearn.ensemble import GradientBoostingRegressor
from sklearn import datasets
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

loc_train = "//home//harini//Kaggle_data//shop//train.csv"
loc_test = "//home//harini//Kaggle_data//shop//test.csv"
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
	print("Finished generating balanced split samples")
	return np.concatenate((train_inds,test_inds),axis=1)
	
def generate_cv_indices_unbalanced(category):
	N = len(category)
	u, indices = np.unique(category, return_inverse=True)
	#print(u)
	train_inds = np.repeat([False],N)
	test_inds = np.repeat([False],N)
	start = 0
	half_data = np.floor(N/2)
	for i in range(0,len(u)):
		i_inds = np.where(indices == i)
		if(np.sum(train_inds)<half_data):
			train_inds[i_inds[0]] = True
		else:
			test_inds[i_inds[0]] = True
	print(np.sum(train_inds))
	print(np.sum(test_inds))
	print("Finished generating unbalanced split samples")
	return np.concatenate((train_inds,test_inds),axis=1)
	
	
	
def svm_cross_validate_category(X,y,category,C,penalty):
	
	clf_svm_1 = GradientBoostingRegressor(loss="huber",n_estimators=C, learning_rate=0.1,alpha=0.5)
	clf_svm_2 = GradientBoostingRegressor(loss="huber",n_estimators=C, learning_rate=0.1,alpha=0.5)
	
	cv_indices = generate_cv_indices(category)
	
	train_ids = cv_indices[0:N]
	test_ids = cv_indices[N:2*N]
	
	clf_svm_1.fit(X[train_ids,:], y[train_ids])
	clf_svm_2.fit(X[test_ids,:], y[test_ids])
	
	score = np.zeros(2)
	score[0] = clf_svm_1.score(X[test_ids,:], y[test_ids])
	score[1] = clf_svm_2.score(X[train_ids,:], y[train_ids])
	mean_score = np.mean(score)
	
	y_1 = clf_svm_1.predict(X[test_ids,:])
	y_2 = clf_svm_2.predict(X[train_ids,:])
	
	u, indices = np.unique(category, return_inverse=True)
	auc = np.zeros((2,len(u)))
	for i in range(0,len(u)):
		
		i_inds = indices == i
		
		if(np.sum(test_ids & i_inds)!=0):
			fpr, tpr, thresholds = metrics.roc_curve(y[test_ids & i_inds], y_1[i_inds[test_ids],1], pos_label=1)
			auc[0,i] = metrics.auc(fpr, tpr)

		if(np.sum(train_ids & i_inds)!=0):
			fpr, tpr, thresholds = metrics.roc_curve(y[train_ids & i_inds], y_2[i_inds[train_ids],1], pos_label=1)
			auc[1,i] = metrics.auc(fpr, tpr)	
	
		mean_auc = np.mean(auc,axis=0)
	print("Finished running category cross-validation")
	return mean_auc

def svm_cross_validate(X,y,category,C,penalty):
	
	clf_svm_1 = GradientBoostingRegressor(loss="huber",n_estimators=C, learning_rate=0.1,alpha=0.5)
	clf_svm_2 = GradientBoostingRegressor(loss="huber",n_estimators=C, learning_rate=0.1,alpha=0.5)
	
	#N = len(category)
	#half_data= np.floor(N/2)
	#cv_indices_1= np.repeat([False],N)
	#cv_indices_2= np.repeat([False],N)
	#cv_indices_1[0:half_data] =True
	#cv_indices_2[half_data:N] =True
	#cv_indices= np.concatenate((cv_indices_1,cv_indices_2),axis=1)
	
	cv_indices = generate_cv_indices_unbalanced(category)
	
	train_ids = cv_indices[0:N]
	test_ids = cv_indices[N:2*N]
	
	clf_svm_1.fit(X[train_ids,:], y[train_ids])
	clf_svm_2.fit(X[test_ids,:], y[test_ids])
	
	score = np.zeros(2)
	score[0] = clf_svm_1.score(X[test_ids,:], y[test_ids])
	score[1] = clf_svm_2.score(X[train_ids,:], y[train_ids])
	mean_score = np.mean(score)
	
	y_1 = clf_svm_1.predict(X[test_ids,:])
	y_2 = clf_svm_2.predict(X[train_ids,:])
	
	auc = np.zeros(2)
	fpr, tpr, thresholds = metrics.roc_curve(y[test_ids], y_1, pos_label=1)
	auc[0] = metrics.auc(fpr, tpr)

	fpr, tpr, thresholds = metrics.roc_curve(y[train_ids], y_2, pos_label=1)
	auc[1] = metrics.auc(fpr, tpr)	
	
	mean_auc = np.mean(auc,axis=0)
	print("Finished running standard cross validation")
	return mean_auc
	

 
def get_category_interactions(X,category,header):
	category_cols = np.array([0,1,2,6,7,8,12,13,14,15,20,21,22])
	u, indices = np.unique(category, return_inverse=True)
	np.savetxt("traincategories.csv", u, fmt="%d,")
	X_indicator =  np.zeros((len(category),len(u)))

	for i in range(0,len(u)):
		X_indicator[indices==i,i] = 1
	X_interaction =  np.zeros((len(category),len(u)*len(category_cols)))

	count = 0
	for i in range(0,len(u)):
		for j in range(0,len(category_cols)):
			X_interaction[:,count] = X_indicator[:,i]*X[:,category_cols[j]]
			new_header = header[category_cols[j]]+"_"+str(u[i])
			header.append(new_header)
			count += 1
	print("Finished generating interaction variables for train")	
	return (X_interaction,header)

def get_category_interactions_test(X,category):
	category_cols = np.array([0,1,2,6,7,8,12,13,14,15,20,21,22])
	
	u, indices = np.unique(category, return_inverse=True)
	train_categories = np.genfromtxt("traincategories.csv", delimiter = ',') 
	u_common = np.intersect1d(u,train_categories)
	print(u_common)
	
	X_indicator =  np.zeros((len(category),len(train_categories)))

	for i in range(0,len(train_categories)):
		X_indicator[[category==train_categories[i]],i] = 1
	
	X_interaction =  np.zeros((len(category),len(train_categories)*len(category_cols)))
	count = 0
	for i in range(0,len(train_categories)):
		for j in range(0,len(category_cols)):
			X_interaction[:,count] = X_indicator[:,i]*X[:,category_cols[j]]
			count += 1
	print("Finished generating interaction variables for test")
	return (X_interaction)
						
 
X, y, category, header, ids = extract_data(loc_train)
#X_interaction,header = get_category_interactions(X,category,header)
#X = np.concatenate((X,X_interaction),axis=1)



[N,m] = X.shape
#corr_X_y = np.corrcoef(np.concatenate((X,y),axis=1),rowvar=0)
#plt.pcolor(corr_X_y, vmin=0, vmax=1)
#plt.colorbar()		
#plt.show()

#count=0
#for e,x in enumerate(header):
	#if (x == "label" or x == "id" or x == "category" or x == ""):
		#print(e,x,"nan")
		#count += 1
		#continue
	#print(e,x,corr_X_y[m,e-count])
		
#X = StandardScaler().fit_transform(X)
y = np.ravel(y)


# change number of estimators
for i, C in enumerate(10. ** np.arange(1, 3)):
	print(C)
    # turn down tolerance for short training time
	cv_auc =svm_cross_validate(X,y,category,int(C),'l1')
	print("The cv auc for C=%1.4f is %1.4f"% (C,np.mean(cv_auc)))
	print(cv_auc)
   
  
# final training and testing
clf_svm = GradientBoostingRegressor(loss="huber",n_estimators=100, learning_rate=0.1,alpha=0.5)
clf_svm.fit(X,y)

#coef_svm = clf_svm.coef_.ravel()
	
#count=0
#outline=""
#out_coeffs = open("coeffs_05062014_l2.csv", "w+")
#for e,x in enumerate(header):
	#if (x == "label" or x == "id" or x == "category" or x ==""):
		#print(e,x,"nan")
		#count += 1
		#continue
	#print(e,x,coef_svm[e-count])
	#outline += x+","+str(coef_svm[e-count])+"\n"
#out_coeffs.write( outline )
#out_coeffs.close()	
	


y_train = clf_svm.predict(X)
print(np.sum(y_train))
submission = np.array([ids,y_train])
submission= np.transpose(submission)

np.savetxt("temp.csv", submission, fmt="%d,%1.6f")


X_test, y_test, category_test, header_test, id_test = extract_data(loc_test)
#X_test_interactions = get_category_interactions_test(X_test,category_test)
#X_test = np.concatenate((X_test, X_test_interactions),axis=1)
X_test = StandardScaler().fit_transform(X_test)

y_test = clf_svm.predict(X_test)

submission = np.array([id_test,y_test])
submission= np.transpose(submission)

np.savetxt("testsubmission.csv", submission, fmt="%d,%1.6f")

