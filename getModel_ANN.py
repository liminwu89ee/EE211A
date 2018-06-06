# -*- coding: utf-8 -*-
"""
Created on Mon May 21 21:09:25 2018
s
@author: WLM-PC
"""


import numpy as np
import pandas as pa
from sklearn.neural_network import MLPClassifier


def getModel_ANN( y, x, pixels):
    
    target = np.asarray(y).reshape((-1,1))
    npx = np.asarray(x)
    nppixels = np.asarray(pixels)
    # X, Y, Z, radial, azimuthal(radius), polar(radius), Pixels(len = 6*windowSize^2)
    data = np.concatenate((npx, nppixels), axis=1)
    #data = np.delete(data, np.s_[0:6], axis=1)
    print("Input shape = ")
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
    print(data_train.shape)
    print(target_train.shape)
    print(data_test.shape)
    print(target_test.shape)
    
    print(data_train)
    print(target_train)
    
    # value(True/False), X, Y, Z, radial, azimuthal(radius), polar(radius), Pixels(len = 6*windowSize^2)
    inputSize = len(data[0])
    mlp = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, alpha=1e-4,
                    solver='sgd', verbose=10, tol=1e-6, random_state=1,
                    learning_rate_init=.1)
    
    
    mlp.fit(data_train, target_train.ravel())
    print("Training set score: %f" % mlp.score(data_train, target_train.ravel()))
    print("Test set score: %f" % mlp.score(data_test, target_test.ravel()))