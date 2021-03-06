# usage: python stream_acc.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import platform
import sys

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

    libmetawear.mbl_mw_sensor_fusion_set_mode(s.device.board, SensorFusionMode.NDOF);
    libmetawear.mbl_mw_sensor_fusion_set_acc_range(s.device.board, SensorFusionAccRange._8G)
    libmetawear.mbl_mw_sensor_fusion_set_gyro_range(s.device.board, SensorFusionGyroRange._2000DPS)
    libmetawear.mbl_mw_sensor_fusion_write_config(s.device.board)

    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.QUATERNION);
    libmetawear.mbl_mw_datasignal_subscribe(signal, None, s.callback)

    libmetawear.mbl_mw_sensor_fusion_enable_data(s.device.board, SensorFusionData.QUATERNION);
    libmetawear.mbl_mw_sensor_fusion_start(s.device.board);

sleep(100.0)

for s in states:
    libmetawear.mbl_mw_sensor_fusion_stop(s.device.board);

    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.QUATERNION);
    libmetawear.mbl_mw_datasignal_unsubscribe(signal)
    libmetawear.mbl_mw_debug_disconnect(s.device.board)

print("Total Samples Received")
for s in states:
    print("%s -> %d" % (s.device.address, s.samples))
