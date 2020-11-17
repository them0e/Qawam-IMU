# usage: python led.py [mac]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

#import sys
#sys.argv[1]



#device = MetaWear("FB:81:71:31:92:7A")
device = MetaWear("C2:9B:59:07:56:C9")
device.connect()
print("Connected")


pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)
libmetawear.mbl_mw_led_play(device.board)

sleep(5.0)

libmetawear.mbl_mw_led_stop_and_clear(device.board)
sleep(1.0)

device.disconnect()
sleep(1.0)
