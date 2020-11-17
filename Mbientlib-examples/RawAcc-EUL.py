# usage: python stream_acc.py [mac1] [mac2] ... [mac(n)]]
# Raw data for euler angles and acceleration stream.
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp_int, create_voidp
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import numpy as np
import platform
import sys


global ax, ay, az
global pitch, roll, heading

pitch =np.array(0)
roll =np.array(0)
heading =np.array(0)
ax=np.array(0)
ay=np.array(0)
az=np.array(0)
# roll, heading = np.array(0)
# ax, ay, az= np.array(0)

e = Event()

if sys.version_info[0] == 2:
    range = xrange

class State:
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.callbackax = FnVoid_VoidP_DataP(self.data_handlerax)

    def data_handler(self, ctx, data):
        global pitch, roll, heading
        # print("%s -> %s" % (self.device.address, parse_value(data)))
        self.samples+= 1
        z = parse_value(data)
        pitch = np.append(pitch, [z.pitch])
        roll = np.append(roll, [z.roll])
        heading = np.append(heading, [z.heading])
    def data_handlerax(self, ctx, data):
        global ax, ay, az
        # print("%s -> %s" % (self.device.address, parse_value(data)))
        self.samples += 1
        z = parse_value(data)
        ax = np.append(ax, [z.x])
        ay = np.append(ay, [z.y])
        az = np.append(az, [z.z])
        print(az)
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

    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.EULER_ANGLE);
    libmetawear.mbl_mw_datasignal_subscribe(signal, None, s.callback)

    # Get the linear accelerometer data signal
    acc = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.LINEAR_ACC)
    # setup threshold detector - detect anything above 1
    # print("ths")
    # ths = libmetawear.mbl_mw_dataprocessor_threshold_create(acc, ThresholdMode.BINARY, 0.2 , 0.0, None, s.callbackax)
    libmetawear.mbl_mw_datasignal_subscribe(acc, None, s.callbackax)
    print("ths ended")
    libmetawear.mbl_mw_sensor_fusion_enable_data(s.device.board, SensorFusionData.EULER_ANGLE);
    libmetawear.mbl_mw_sensor_fusion_enable_data(s.device.board, SensorFusionData.LINEAR_ACC);
    libmetawear.mbl_mw_sensor_fusion_start(s.device.board);
    print("start streaming")

sleep(5.0)

for s in states:
    print("stop streaming")
    libmetawear.mbl_mw_sensor_fusion_stop(s.device.board);

    libmetawear.mbl_mw_acc_stop(s.device.board)
    libmetawear.mbl_mw_acc_disable_acceleration_sampling(s.device.board)

    print("Unsubscribing.. ")
    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.EULER_ANGLE)
    libmetawear.mbl_mw_datasignal_unsubscribe(signal)
    acc = libmetawear.mbl_mw_sensor_fusion_get_data_signal(s.device.board, SensorFusionData.LINEAR_ACC)
    print("ths")
    ths = libmetawear.mbl_mw_dataprocessor_threshold_create(acc, ThresholdMode.BINARY, 0.2, 0.0, None, s.callbackax)
    libmetawear.mbl_mw_datasignal_unsubscribe(ths)
    print("ths ended")


    libmetawear.mbl_mw_debug_disconnect(s.device.board)

print("Total Samples Received")
for s in states:
    print("%s -> %d" % (s.device.address, s.samples))
    print(az)
