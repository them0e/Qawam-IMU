#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'accelerometer_logging.py'
==================
Updated by dmatthes1982 <dmatthes@cbs.mpg.de>
Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2018-04-20
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import json
import time

from pymetawear.discover import select_device
from pymetawear.client import MetaWearClient
from pymetawear.exceptions import PyMetaWearException, PyMetaWearDownloadTimeout
from mbientlab.metawear.cbindings import SensorFusionData, SensorFusionGyroRange, SensorFusionAccRange, SensorFusionMode

address = select_device()

c = MetaWearClient(str(address), debug=True)
print("New client created: {0}".format(c))

#settings = c.accelerometer.get_possible_settings()
#sett = c.sensorfusion.get_possible_settings()

#print("Possible accelerometer settings of client:")
#for k, v in settings.items():
#    print(k, v)

#print("Write accelerometer settings...")
#c.accelerometer.set_settings(data_rate=400, data_range=4.0)

#settings = c.accelerometer.get_current_settings()

c.sensorfusion.set_mode(SensorFusionMode.NDOF)
c.sensorfusion.set_sig(SensorFusionData.EULER_ANGLE)
#c.sensorfusion.get_data_signal(SensorFusionData.EULER_ANGLE)
print("Set Time Processor to limit data rate to 50Hz for each channel")
c.sensorfusion.set_sample_delay(SensorFusionData.EULER_ANGLE, 20)

print("Subscribing to Sensor Fusion Quaternion signal notifications...")
c.sensorfusion.start_logging()

#c.accelerometer.high_frequency_stream = False
#c.accelerometer.start_logging()
#c.sensorfusion.start_logging()
print("Logging accelerometer data...")

time.sleep(3.0)

c.sensorfusion.stop_logging()
print("Logging stopped.")

print("Downloading data...")
download_done = False
n = 0
data = None
while (not download_done) and n < 3:
    try:
        data = c.sensorfusion.download_log()
        download_done = True
    except PyMetaWearDownloadTimeout:
        print("Download of log interrupted. Trying to reconnect...")
        c.disconnect()
        c.connect()
        n += 1
if data is None:
    raise PyMetaWearException("Download of logging data failed.")

for d in data:
    print(d)
    #v = d['value']



# print(str(v))
# dat = str(v)
# print(type(dat))
# #print(dat[4:10])
# x = float(dat[4:10])
# print(x)
# print(type(x))
# #print(dat[15:22])
# y = float(dat[15:22])
# print(y)
# #print(dat[27:33])
# z = float(dat[27:33])
# print(z)
print("Disconnecting...")
c.disconnect()

# class MetaWearDataEncoder(json.JSONEncoder):
#     """JSON Encoder for converting ``mbientlab`` module's CartesianFloat
#     class to data tuple ``(x,y,z)``."""
#     def default(self, o):
#         if isinstance(o, CartesianFloat):
#             return o.x, o.y, o.z
#         else:
#             return super(MetaWearDataEncoder, self).default(o)
#
# data_file = os.path.join(os.getcwd(), "logged_data.json")
# print("Saving the data to file: {0}".format(data_file))
# with open("logged_data.json", "wt") as f:
#     json.dump(data, f, indent=2)