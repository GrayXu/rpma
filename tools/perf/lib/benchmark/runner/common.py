#!/usr/bin/env python3
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021, Intel Corporation
#

#
# common.py
#

"""the runner's helpers (EXPERIMENTAL)"""

import json

#: an error message when an unexpected mode is detected
UNKNOWN_MODE_MSG = "An unexpected 'mode' value: {}"

#: an error message when x-axis cannot be identified
NO_X_AXIS_MSG = \
    "SETTINGS_BY_MODE[{}] is missing a key defined as a list (x-axis)"

#: a common block sizes list
BS_VALUES = [256, 1024, 4096, 8192, 16384, 32768, 65536, 131072, 262144]

def result_append(data: list, idfile: str, result: dict) -> None:
    """append new result to internal data and file"""
    data.append(result)
    with open(idfile, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def result_is_done(data: list, x_key: str, x_value: int) -> bool:
    """check if the result for the given x_value of x_key is already collected"""
    for result in data:
        # A result can be a tuple (read, write) or a list of two elements
        # in case of the fio 'rw' mode and then it is enough to check
        # only the first item, because they both have to have the same keys.
        if isinstance(result, (tuple, list)):
            result = result[0]
        if x_key not in result:
            raise ValueError('key \'{}\' is missing the previous results'
                             .format(x_key))
        if str(result[x_key]) == str(x_value):
            return True
    return False

def print_start_message(mode, oneseries, config):
    """print the STARTING message"""
    tool = oneseries['tool']
    if 'tool_mode' in oneseries:
        tool = tool + '({})'.format(oneseries['tool_mode'])
    print('STARTING benchmark TOOL={} for MODE={} (IP={}) ...'
          .format(tool, mode, config['server_ip']))
