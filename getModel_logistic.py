# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:16:56 2018
s
@author: WLM-PC
"""
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pa
from sklearn.neural_network import MLPClassifier
import sklearn
from sklearn import svm


def getModel_logistic( y, x, pixels):
    
    target = np.array(y).reshape((-1,1))
    print("target size:")
    print(target.shape)
    
    npx = np.array(x)
    print("npx size:")
    print(npx.shape)
    
    nppixels = np.asarray(pixels)
    print("nppixels size:")
    print(nppixels.shape)    
    
    # X, Y, Z, radial, azimuthal(radius), polar(radius), Pixels(len = 6*windowSize^2)
    data = np.concatenate((npx, nppixels), axis=1)
    #data = np.delete(data, np.s_[0:6], axis=1)
    print("Input shape:")
    print(data.shape)
    
    num_train = len(target)
    num_folds = 5 # 20% testing, 80% training
    
    cv_idx = np.arange(num_train)
    np.random.shuffle(cv_idx)
    fold_size = num_train//num_folds
    test_idx = cv_idx[0:fold_size]
    train_idx = cv_idx[fold_size:]
    data_train = data[train_idx]
    target_train = target[train_idx]
    data_test = data[test_idx]
    target_test = target[test_idx]
    
    print("data_train shape:")
    print(data_train.shape)
    print("target_train shape:")
    print(target_train.shape)
    print("data_test shape:")
    print(data_test.shape)
    print("target_test shape:")
    print(target_test.shape)
    
    #print(data_train)
    #print(target_train)
    
    # value(True/False), X, Y, Z, radial, azimuthal(radius), polar(radius), Pixels(len = 6*windowSize^2)
    inputSize = len(data[0])
    clf = sklearn.linear_model.LogisticRegression()
    
    clf.fit(data_train,target_train)
    
    target_pred = clf.predict(data_test)
    print(np.mean(target_pred==target_test))
    cnf_matrix = confusion_matrix(target_test, target_pred)
    print(cnf_matrix)
    
    print("Training set score: %f" % clf.score(data_train, target_train.ravel()))
    print("Test set score: %f" % clf.score(data_test, target_test.ravel()))
    
    return clf