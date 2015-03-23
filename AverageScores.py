#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
# Read train and test data and run Logistic regression

import numpy as np
import pylab as pl

huber_file="testsubmission_modified_huber_05172014.csv"
modified_huber_file="testsubmission_randomforest_05172014.csv"

modified_huber_data = np.genfromtxt(modified_huber_file, delimiter = ',') 
[N,m] = modified_huber_data.shape

huber_data = np.genfromtxt(huber_file, delimiter = ',') 
[N,m] = huber_data.shape

print(huber_data.shape)

average_score = 0.5*modified_huber_data[:,1]+0.5*huber_data[:,1]
submission = np.array([modified_huber_data[:,0],average_score])
submission= np.transpose(submission)

np.savetxt("testsubmission_average_05182014.csv", submission, fmt="%d,%1.6f")


