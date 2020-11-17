# usage: python battery_test.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import platform
import sys

# device = MetaWear('FB:81:71:31:92:7A')
# device.connect()



if sys.version_info[0] == 2:
    range = xrange

class State:
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)

    def data_handler(self, ctx, data):
        print("%s -> %s" % (self.device.address, parse_value(data)))
        self.samples+= 1

states = []
for i in range(len(sys.argv) - 1):
    d = MetaWear(sys.argv[i + 1])
    d.connect()
    print("Connected to " + d.address)
    states.append(State(d))

for s in states:
    print("Configuring device")
    libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
    sleep(1.5)





# Callback function to process/parse the battery data
# def data_handler(self, ctx, data):
#     print("%s -> %s" % (self.device.address, parse_value(data)))
#
# callback = FnVoid_VoidP_DataP(data_handler)
# print("Configuring device")
# libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
    print("Subscribing to the signal")
    battery_signal = libmetawear.mbl_mw_settings_get_battery_state_data_signal(s.device.board)
    libmetawear.mbl_mw_datasignal_subscribe(battery_signal, None, s.callback)

    sleep(1.0)
    print("Reading the signal")
    # The loop's range is the desired number of samples
    for i in range(2500):
        libmetawear.mbl_mw_datasignal_read(battery_signal)
        # Period of time.
        sleep(0.5)



for s in states:
    libmetawear.mbl_mw_datasignal_unsubscribe(battery_signal)
    libmetawear.mbl_mw_debug_disconnect(s.device.board)

    s.device.on_disconnect = lambda status: print("we are disconnected!")
    s.device.disconnect()

print("Total Samples Received")
for s in states:
    print("%s -> %d" % (s.device.address, s.samples))