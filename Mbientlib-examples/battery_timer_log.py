# usage: python log_temp.py [mac]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value, create_voidp, create_voidp_int
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import sys

print("Searching for device...")
d = MetaWear(sys.argv[1])
d.connect()
print("Connected to " + d.address)

try:
    e = Event()

    print("Configuring device")
    # logging
    battery_signal = libmetawear.mbl_mw_settings_get_battery_state_data_signal(d.board)
    logger = create_voidp(lambda fn: libmetawear.mbl_mw_datasignal_log(battery_signal, None, fn), resource="battery_logger",
                          event=e)

    # mbl_mw_timer_create_indefinite(
    # MblMwMetaWearBoard * board, uint32_t period, uint8_t  delay, void * context, MblMwFnTimerPtr received_timer
    # )
    #
    # Creates a timer that will run indefinitely.
    # Period is in 1/1000sec
    # Delay: 0 if the timer should immediately fire, non-zero to delay the first event.
    timer = create_voidp(lambda fn: libmetawear.mbl_mw_timer_create_indefinite(d.board, 1000, 0, None, fn),
                         resource="timer", event=e)
    libmetawear.mbl_mw_event_record_commands(timer)
    libmetawear.mbl_mw_datasignal_read(battery_signal)
    create_voidp_int(lambda fn: libmetawear.mbl_mw_event_end_record(timer, None, fn), event=e)

    libmetawear.mbl_mw_logging_start(d.board, 0)
    libmetawear.mbl_mw_timer_start(timer)

    print("Logging data for 15s")
    sleep(15.0)

    libmetawear.mbl_mw_timer_remove(timer)
    libmetawear.mbl_mw_logging_stop(d.board)

    print("Downloading data")
    libmetawear.mbl_mw_settings_set_connection_parameters(d.board, 7.5, 7.5, 0, 6000)
    sleep(1.0)


    def progress_update_handler(context, entries_left, total_entries):
        if (entries_left == 0):
            e.set()


    fn_wrapper = FnVoid_VoidP_UInt_UInt(progress_update_handler)
    download_handler = LogDownloadHandler(context=None, \
                                          received_progress_update=fn_wrapper, \
                                          received_unknown_entry=cast(None, FnVoid_VoidP_UByte_Long_UByteP_UByte), \
                                          received_unhandled_entry=cast(None, FnVoid_VoidP_DataP))

    callback = FnVoid_VoidP_DataP(lambda ctx, p: print("{epoch: %d, value: %s}" % (p.contents.epoch, parse_value(p))))
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
