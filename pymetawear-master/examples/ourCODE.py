#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`sensorfusion`
==================
Created by mgeorgi <marcus.georgi@kinemic.de>
Created on 2016-02-01
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time
import numpy as np
from functools import partial

# from mpl_toolkits import mplot3d
# %matplotlib inline
# import matplotlib.pyplot as plt

from pymetawear.discover import select_device
from pymetawear.client import MetaWearClient
from mbientlab.metawear.cbindings import SensorFusionData, SensorFusionGyroRange, SensorFusionAccRange, SensorFusionMode

global ACC_x
global ACC_y
global ACC_z
global EU_pitch
global EU_roll
global EU_yaw

#address = select_device()
c = MetaWearClient(str('C2:9B:59:07:56:C9'), debug=True)
# c = MetaWearClient(str('FB:81:71:31:92:7A'), debug=True)
print("New client created: {0}".format(c))


ACC_x = np.array(0)
ACC_y = np.array(0)
ACC_z = np.array(0)
EU_pitch = np.array(0)
EU_roll = np.array(0)
EU_yaw = np.array(0)


def status_detection(z):

    # Status
    s = 0  # sitting
    # t = np.array(
    print("This is Z: ")
    print(z)
    # Find values over 0.15 (jumps)
    # x_c = np.where(abs(x) > 0.15)
    # y_c = np.where(abs(y) > 0.15)
    z_c = np.where(abs(z) > 0.15)
    print("z_c BEFORE:")
    print(z_c)
    print("length of z_c = ")
    print(np.shape(z_c))
    z_c = np.reshape(z_c, -1)
    print("z_c AFTER: ")
    print(z_c)
    # z_c = np.nonzero(z_c)
    # status pointer;
    sp = np.array(0)
    print("length of z_c = ")
    # print(np.shape(z_c)[1])
    print(np.shape(z_c))
    # z_c = z_c[:1]


    # iterate through all indices of values above 0.15
    # subtract the next index from the current index; if the result was larger the 40 (threshold = 40 indices)
    # this jump in indices represents a change in a person status from sitting to standing (or vice-versa).

    iters = np.shape(z_c)[0]
    print(iters)
    #  if(np.shape(z_c) != 0):
    for i in range(iters - 1):
        # print((z_c[i+1] - z_c[i]))
        if (z_c[i + 1] - z_c[i]) > 20:
            sp = np.append(sp, z_c[i])
            print("CHANGE")
    print("CHANGE")
    print(sp)

def handle_notificationACC(data, type_=''):

    global ACC_x
    global ACC_y
    global ACC_z


    #print("{0}: {1}".format(type_, data))


    v = data['value']
    ACC_x = np.append(ACC_x,[v.x])
    ACC_y = np.append(ACC_y,[v.y])
    ACC_z = np.append(ACC_z,[v.z])

    # print(v.x)
    # print(type(v.x))
    #print(data['value'])
    #v = data['value']

    # print(str(v))
    #dat = str(v)
    # print(type(dat))
    # #print(dat[4:10])
    #x = float(dat[4:10])

    #print(x)
    # print(type(x))
    # #print(dat[15:22])
    # y = float(dat[15:22])
    # print(y)
    # #print(dat[27:33])
    # z = float(dat[27:33])
    # print(z)


def handle_notificationEU(data, type_=''):
    # print("{0}: {1}".format(type_, data))
    #print(data['value'])

    global EU_pitch
    global EU_roll
    global EU_yaw

    v = data['value']
    EU_pitch = np.append(EU_pitch,[v.pitch])
    EU_roll = np.append(EU_roll,[v.roll])
    EU_yaw = np.append(EU_yaw,[v.yaw])

    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.plot3D(EU_pitch, EU_roll, EU_yaw, 'gray')
    # ax.scatter3D(EU_pitch, EU_roll, EU_yaw, c=EU_yaw, cmap='Greens')
    # # print(str(v))
    # dat = str(v)
    # # print(type(dat))
    # # #print(dat[4:10])
    # x = float(dat[4:10])
    #
    # print(x)
    # print(type(x))
    # #print(dat[15:22])
    # y = float(dat[15:22])
    # print(y)
    # #print(dat[27:33])
    # z = float(dat[27:33])
    # print(z)
def handle_notification2(data):
    print("2: {0}".format(data))

# def battery_callback(data):
#     epoch = data[0]
#     battery = data[1]
#     print("[{0}] Voltage: {1}, Charge: {2}".format(
#         epoch, battery[0], battery[1]))
print("Write Sensor Fusion settings...")
c.sensorfusion.set_mode(SensorFusionMode.NDOF)
#c.sensorfusion.set_acc_range(SensorFusionAccRange._8G)
#c.sensorfusion.set_gyro_range(SensorFusionGyroRange._1000DPS)
#c.settings.notifications(handle_notification(lambda data: handle_notification2(data)))

print("Set Time Processor to limit data rate to 50Hz for each channel")
c.sensorfusion.set_sample_delay(SensorFusionData.EULER_ANGLE, 20)
#c.sensorfusion.set_sample_delay(SensorFusionData.QUATERNION, 20)
c.sensorfusion.set_sample_delay(SensorFusionData.LINEAR_ACC, 20)
#c.sensorfusion.set_sample_delay(SensorFusionData.CORRECTED_GYRO, 20)
time.sleep(2)
print("Subscribing to Sensor Fusion Quaternion signal notifications...")
#c.sensorfusion.notifications(euler_angle_callback=handle_notification)
#c.sensorfusion.notifications(quaternion_callback=handle_notification)
c.sensorfusion.notifications(
    linear_acc_callback=partial(handle_notificationACC, type_='Acc '),
    #quaternion_callback=partial(handle_notification, type_='Quat'),
    #corrected_gyro_callback=partial(handle_notification, type_='Gyro'),
    euler_angle_callback=partial(handle_notificationEU, type_='Euler'))


# print("Subscribe to battery notifications...")
# c.settings.notifications(lambda data: print(data))

# time.sleep(1.0)

# print("Trigger battery state notification...")
# c.settings.read_battery_state()
#time.sleep(2.0)

#c.sensorfusion.notifications(quaternion_callback=handle_notification2)

time.sleep(20.0)

print("Unsubscribe to notification...")
c.sensorfusion.notifications()
#c.settings.notifications(None)

# print(ACC_x)
# print(ACC_y)
# print(ACC_z)
#print(EU_yaw)
status_detection(ACC_z)
# np.savetxt("ACC_z.csv", ACC_z, delimiter=",")
np.savetxt("EU.csv", (EU_pitch, EU_roll, EU_yaw), delimiter=",")
time.sleep(5.0)

c.disconnect()