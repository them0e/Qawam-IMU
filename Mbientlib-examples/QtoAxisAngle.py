from pyquaternion import Quaternion
import numpy as np
import pandas as pd

# Preprocessing Input data
data = pd.read_csv('FBLR.csv')
# all four dimensions as a 4D numpy array
allds = data.iloc[:, 3:].values
# Time Elapsed as a numpy array
te = data.iloc[:, 2:3].values

# X, Y, Z, and W
W = data.iloc[:, 3:4].values
X = data.iloc[:, 4:5].values
Y = data.iloc[:, 5:6].values
Z = data.iloc[:, 6:7].values

