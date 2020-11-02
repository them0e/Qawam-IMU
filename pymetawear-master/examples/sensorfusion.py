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
from functools import partial

from pymetawear.discover import select_device
from pymetawear.client import MetaWearClient
from mbientlab.metawear.cbindings import SensorFusionData, SensorFusionGyroRange, SensorFusionAccRange, SensorFusionMode

address = select_device()
c = MetaWearClient(str(address), debug=True)
print("New client created: {0}".format(c))

def handle_notification(data, type_=''):
    print("{0}: {1}".format(type_, data))
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


def handle_notification3(data, type_=''):
     print("{0}: {1}".format(type_, data))
    # v = data['value']
    #
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
c.sensorfusion.set_sample_delay(SensorFusionData.CORRECTED_ACC, 20)
#c.sensorfusion.set_sample_delay(SensorFusionData.CORRECTED_GYRO, 20)

print("Subscribing to Sensor Fusion Quaternion signal notifications...")
#c.sensorfusion.notifications(euler_angle_callback=handle_notification)
#c.sensorfusion.notifications(quaternion_callback=handle_notification)
c.sensorfusion.notifications(
    corrected_acc_callback=partial(handle_notification, type_='Acc '),
    #quaternion_callback=partial(handle_notification, type_='Quat'),
    #corrected_gyro_callback=partial(handle_notification, type_='Gyro'),
    euler_angle_callback=partial(handle_notification3, type_='Euler'))


# print("Subscribe to battery notifications...")
# c.settings.notifications(lambda data: print(data))

time.sleep(1.0)

# print("Trigger battery state notification...")
# c.settings.read_battery_state()
#time.sleep(2.0)

#c.sensorfusion.notifications(quaternion_callback=handle_notification2)

time.sleep(5.0)

print("Unsubscribe to notification...")
c.sensorfusion.notifications()
c.settings.notifications(None)
time.sleep(5.0)

c.disconnect()