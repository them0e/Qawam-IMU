# usage: python stream_acc.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import platform
import sys

device = MetaWear('FB:81:71:31:92:7A')
device.connect()






# Callback function to process/parse the battery data
def data_handler(self, ctx, data):
    print("%s -> %s" % (self.device.address, parse_value(data)))

callback = FnVoid_VoidP_DataP(data_handler)
print("Configuring device")
libmetawear.mbl_mw_settings_set_connection_parameters(device.board, 7.5, 7.5, 0, 6000)

battery_signal = libmetawear.mbl_mw_settings_get_battery_state_data_signal(device.board)
libmetawear.mbl_mw_datasignal_subscribe(battery_signal, None, callback)

sleep(1.0)

libmetawear.mbl_mw_datasignal_read(battery_signal)

sleep(5.0)

libmetawear.mbl_mw_datasignal_unsubscribe(battery_signal)
libmetawear.mbl_mw_debug_disconnect(device.board)

device.on_disconnect = lambda status: print("we are disconnected!")
device.disconnect()