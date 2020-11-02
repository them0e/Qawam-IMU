# Testing algorithms

import numpy as np
import csv
from mpl_toolkits import mplot3d
# %matplotlib inline
import matplotlib.pyplot as plt

def status_detection(z1):

    # Status
    s = 0 #sitting
    #t = np.array(

    # Find values over 0.15 (jumps)
    # x_c = np.where(abs(x) > 0.15)
    # y_c = np.where(abs(y) > 0.15)
    z_c = np.where(abs(z1) > 0.15)
    z_c = np.reshape(z_c, -1)
    #z_c = np.nonzero(z_c)
    # status pointer;
    sp = np.array(0)
    print("length of z_c = ")
   # print(np.shape(z_c)[1])
    print(np.shape(z_c))
   # z_c = z_c[:1]
    print("z_c = ")
    print(z_c)

    # iterate through all indices of values above 0.15
    # subtract the next index from the current index; if the result was larger the 40 (threshold = 40 indices)
    # this jump in indices represents a change in a person status from sitting to standing (or vice-versa).

    iters = np.shape(z_c)[0]
    #print(iters)
  #  if(np.shape(z_c) != 0):
    for i in range(iters-1):
         # print((z_c[i+1] - z_c[i]))
         if (z_c[i+1] - z_c[i]) > 100:
             sp = np.append(sp, z_c[i])
             print("CHANGE")
    print(sp)
    #print(z_c)


with open('EU.csv', newline='') as csvfile:
    z = list(csv.reader(csvfile))
z = np.array(z)
z = z.astype(float)
print("Type of z: ")
print(type(z))
print("shape of z = ")
print(np.shape(z))
print(z)
# status_detection(z)
#print(z)
