#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Haptic module
-------------

Created by hbldh <henrik.blidh@nedomkull.com> on 2016-04-14

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import logging
from ctypes import c_float, c_uint16

from pymetawear import libmetawear
from pymetawear.exceptions import PyMetaWearException
from pymetawear.modules.base import PyMetaWearModule

log = logging.getLogger(__name__)


class HapticModule(PyMetaWearModule):
    """MetaWear Haptic module implementation.

    :param ctypes.c_long board: The MetaWear board pointer value.
    :param bool debug: If ``True``, module prints out debug information.

    """

    def __str__(self):
        return "{0}".format(self.module_name)

    def __repr__(self):
        return super(HapticModule, self).__repr__()

    @property
    def module_name(self):
        return 'Haptic'

    def notifications(self, callback=None):
        """No subscriptions possible for Haptic module.

        :raises: :py:exc:`~PyMetaWearException`

        """
        raise PyMetaWearException("Haptic module has no notifications.")

    def start_motor(self, duty_cycle_per, pulse_width_ms):
        """Activate the haptic motor.

        :param float duty_cycle_per: Strength of the motor,
            between [0, 100] percent
        :param int pulse_width_ms: How long to run the motor, in milliseconds

        """
        libmetawear.mbl_mw_haptic_start_motor(
            self.board,
            c_float(float(duty_cycle_per)),
            c_uint16(int(pulse_width_ms)))

    def start_buzzer(self, pulse_width_ms):
        """Activate the haptic buzzer.

        :param int pulse_width_ms: How long to run the motor, in milliseconds

        """
        libmetawear.mbl_mw_haptic_start_buzzer(
            self.board,
            c_uint16(int(pulse_width_ms)))
