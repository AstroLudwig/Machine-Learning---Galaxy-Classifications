# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Machine Learning
PURPOSE:
    Train and Predict on Newly Reduced Data Set
NOTE: 
https://scikit-learn.org/stable/modules/neural_networks_supervised.html#classification
"""
import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd 
from sklearn.neural_network import MLPClassifier

df = pd.read_csv("ML_Ready_Catalog.csv")

X = df.drop(labels="type",axis=1)

X_ = np.asarray(X.loc[0:250000])
Y = df["type"].loc[0:250000]

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(22, 22), random_state=1)

clf.fit(X_, Y)

print(("Actual type {}").format(df["type"].loc[260000]))
test = np.asarray(X.loc[260000])
prediction = clf.predict(test)

print(("Predicted type {}").format(prediction))