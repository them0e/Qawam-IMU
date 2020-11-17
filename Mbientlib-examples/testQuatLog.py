# usage: python log_acc.py [mac]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp, create_voidp_int
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import sys


print("Searching for device...")
d = MetaWear('C2:9B:59:07:56:C9')
d.connect()
print("Connected to " + d.address)

print("Configuring device")

try:
    # sensorfusion.set_mode() function
    libmetawear.mbl_mw_sensor_fusion_set_mode(d.board, SensorFusionMode.NDOF)
    libmetawear.mbl_mw_sensor_fusion_write_config(d.board)


    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(d.board, SensorFusionData.EULER_ANGLE)
    logger = create_voidp(lambda fn: libmetawear.mbl_mw_datasignal_log(signal, None, fn), resource="Euler_logger")

    libmetawear.mbl_mw_logging_start(d.board, 0)
    libmetawear.mbl_mw_sensor_fusion_enable_data(d.board, SensorFusionData.EULER_ANGLE)
    libmetawear.mbl_mw_sensor_fusion_start(d.board)

    print("Logging data for 5s")
    sleep(5.0)

    libmetawear.mbl_mw_sensor_fusion_stop(d.board)
    libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(d.board)
    libmetawear.mbl_mw_logging_stop(d.board)

    print("Downloading data")
    libmetawear.mbl_mw_settings_set_connection_parameters(d.board, 7.5, 7.5, 0, 6000)
    sleep(1.0)

    e = Event()


    def progress_update_handler(context, entries_left, total_entries):
        if (entries_left == 0):
            e.set()


    fn_wrapper = FnVoid_VoidP_UInt_UInt(progress_update_handler)
    download_handler = LogDownloadHandler(context=None, \
                                          received_progress_update=fn_wrapper, \
                                          received_unknown_entry=cast(None, FnVoid_VoidP_UByte_Long_UByteP_UByte), \
                                          received_unhandled_entry=cast(None, FnVoid_VoidP_DataP))

    callback = FnVoid_VoidP_DataP(lambda ctx, p: print("{epoch: %d, value: %s}" % (p.contents.epoch, parse_value(p))))
    sleep(2.0)
    libmetawear.mbl_mw_logger_subscribe(logger, None, callback)
    libmetawear.mbl_mw_logging_download(d.board, 0, byref(download_handler))
    e.wait()

except RuntimeError as err:
    print(err)
finally:
    print("Resetting device")

    e = Event()
    d.on_disconnect = lambda status: e.set()
    libmetawear.mbl_mw_debug_reset(d.board)
    e.wait()