#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:04:25 2020

@author: bmonikraj
"""

import pickle
import pandas as pd
from sklearn.naive_bayes import GaussianNB

MODELFILE = 'clf_model.sav'

df = pd.read_csv("./sonar.all-data", header=None)
df.loc[df[60] =='M', 60] = 1 # code 'M' as 1
df.loc[df[60] =='R', 60] = 0 # code 'R' as 0
y = df.loc[:, 60:]
x = df.drop([60], axis=1)

clf = GaussianNB()
clf.fit(x, y)

pickle.dump(clf, open(MODELFILE, 'wb'))


'''
[0.0269,
 0.0383,
 0.0505,
 0.0707,
 0.1313,
 0.2103,
 0.2263,
 0.2524,
 0.3595,
 0.5915,
 0.6675,
 0.5679,
 0.5175,
 0.3334,
 0.2002,
 0.2856,
 0.2937,
 0.3424,
 0.5949,
 0.7526,
 0.8959,
 0.8147,
 0.7109,
 0.7378,
 0.7201,
 0.8254,
 0.8917,
 0.982,
 0.8179,
 0.4848,
 0.3203,
 0.2775,
 0.2382,
 0.2911,
 0.1675,
 0.3156,
 0.1869,
 0.3391,
 0.5993,
 0.4124,
 0.1181,
 0.3651,
 0.4655,
 0.4777,
 0.3517,
 0.092,
 0.1227,
 0.1785,
 0.1085,
 0.03,
 0.0346,
 0.0167,
 0.0199,
 0.0145,
 0.0081,
 0.0045,
 0.0043,
 0.0027,
 0.0055,
 0.0057]
'''
