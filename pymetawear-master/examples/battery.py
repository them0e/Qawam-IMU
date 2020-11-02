#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`battery`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-04-02

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time

from pymetawear.discover import select_device
from pymetawear.client import MetaWearClient

# def battery_callback(data):
#     epoch = data[0]
#     battery = data[1]
#     print("[{0}] Voltage: {1}, Charge: {2}".format(
#         epoch, battery[0], battery[1]))


address = select_device()
c = MetaWearClient(str(address), debug=True)
print("New client created: {0}".format(c))

print("Subscribe to battery notifications...")
c.settings.notifications(lambda data: print(data))

# print("Subscribe to battery notifications...")
# c.settings.notifications(battery_callback())

time.sleep(1.0)

print("Trigger battery state notification...")
c.settings.read_battery_state()

time.sleep(2.0)

print("Unsubscribe to battery notifications...")
c.settings.notifications(None)

time.sleep(1.0)

c.disconnect()
