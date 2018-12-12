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
clf = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(22, 22), random_state=1,
					max_iter=200000, verbose=True)

# Train the Net
clf.fit(TrainingData, TrainingClass)

# Get the Real Types that haven't been used in training, Validation Set
RealClass = Class.loc[n:df.shape[0]]

# Give the other half of the  data to test the fit
RealData = np.asarray(Data.loc[n:df.shape[0]])

# What type does it think it is? 
PredictClass = clf.predict(RealData)

# How accurate was it?
Accuracy = np.shape(np.where((RealClass - PredictClass)==0))[1] / RealClass.shape[0] * 100

# Root Mean Square Error, how they evaluate the kaggle contest.
N =  df.shape[0] - n
rmse = np.sqrt(np.sum((RealClass - PredictClass)**2)/N)


# A bunch of nonsense to give me an idea of how well I did.
print(("Accuracy {0:.2f}%").format(Accuracy))
print(("Root Mean Squared Error {0:.2f}").format(rmse))
print(" ")
print("For Entire Remainder of the Data Set:")
print(("{0:.2f}% of types are Point Source/Artefacts").format(np.shape(np.where(Class==0))[1]/Class.shape[0]*100))
print(("{0:.2f}% of types are Early Types").format(np.shape(np.where(Class==1))[1]/Class.shape[0]*100))
print(("{0:.2f}% of types are Spirals").format(np.shape(np.where(Class==2))[1]/Class.shape[0]*100))
print(" ")
print("For the Validation Set:")
print(("{0:.2f}% of types are Point Source/Artefacts").format(np.shape(np.where(RealClass==0))[1]/RealClass.shape[0]*100))
print(("{0:.2f}% of types are Early Types").format(np.shape(np.where(RealClass==1))[1]/RealClass.shape[0]*100))
print(("{0:.2f}% of types are Spirals").format(np.shape(np.where(RealClass==2))[1]/RealClass.shape[0]*100))
print(" ")
print("For the Validation Set, the computer thought that:")
print(("{0:.2f}% of types are Point Source/Artefacts").format(np.shape(np.where(PredictClass==0))[1]/PredictClass.shape[0]*100))
print(("{0:.2f}% of types are Early Types").format(np.shape(np.where(PredictClass==1))[1]/PredictClass.shape[0]*100))
print(("{0:.2f}% of types are Spirals").format(np.shape(np.where(PredictClass==2))[1]/PredictClass.shape[0]*100))

# Plot of the histograms 
f, (ax,bx) = plt.subplots(1,2)
ax.hist(RealClass,bins=3,rwidth=1)#[0,1,2,3])
bx.hist(PredictClass,bins=3,rwidth=1)#[0,1,2,3])

plt.show()