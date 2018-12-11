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
import matplotlib.pyplot as plt 
import pandas as pd 
from sklearn.neural_network import MLPClassifier

# Load Data Set 
df = pd.read_csv("ML_Ready_Catalog.csv")

# Split data set up into actual observations and then the type they were determined to be.
Data = df.drop(labels="type",axis=1)
Class = df["type"]

# Use half the data set for training
n = int(df.shape[0]/2)
TrainingData = np.asarray(Data.loc[0:n])
TrainingClass = Class.loc[0:n]

# Create the Neural Net with 2N by 2N hidden layers
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(22, 22), random_state=1)

# Train the Net
clf.fit(TrainingData, TrainingClass)

# Get the Real Types that haven't been used in training
RealClass = Class.loc[n:df.shape[0]]

# Give the other half of the  data to test the fit
RealData = np.asarray(Data.loc[n:df.shape[0]])

# What type does it think it is? 
PredictClass = clf.predict(RealData)

# How accurate was it?
Accuracy = np.shape(np.where((RealClass - PredictClass)==0))[1] / RealClass.shape[0] * 100

print(("Accuracy {:0f}%").format(Accuracy))

f, (ax,bx) = plt.subplots(1,2)
ax.hist(RealClass,bins=3,rwidth=1)#[0,1,2,3])
bx.hist(PredictClass,bins=3,rwidth=1)#[0,1,2,3])

plt.show()