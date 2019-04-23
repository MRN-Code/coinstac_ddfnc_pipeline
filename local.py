#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:08:00 2018 (MDT)

@author: Rogers F. Silva
"""

import ujson as json
import os
import sys
import copy
import numpy as np
import utils as ut
import phase_keys as pk
from constants import OUTPUT_TEMPLATE

LOCAL_GICA_PHASES = \
    pk.ROW_MEANS_LOCAL  # + \
# pk.SPATIALLY_CONSTRAINED_ICA_LOCAL + \
# pk.DFNC_PREPROC_LOCAL + \
# pk.DKMEANS_LOCAL + \
# pk.DFNC_STATS_LOCAL

if __name__ == '__main__':
    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(ut.listRecursive(parsed_args, 'computation_phase'))
    computation_output = copy.deepcopy(OUTPUT_TEMPLATE)
    # #print("After phase %s" % phase_key)
    # #print("Args %s" % parsed_args)
    for expected_phases in LOCAL_GICA_PHASES:
        if expected_phases.get('recv') == phase_key:
            # #print("Doing phase %s" % expected_phases.get('recv'))
            operations = expected_phases.get('do')
            for operation in operations:
                computation_output = operation(parsed_args)
                parsed_args = copy.deepcopy(computation_output)
            actual_cp = computation_output.get('output').get(
                'computation_phase')
            expected_cp = expected_phases.get('send')
            # raise (Exception(
            #     "Expected - %s - GOT - %s - %s" %
            #     (expected_cp, actual_cp, expected_cp == actual_cp)))
            assert (actual_cp == expected_cp), \
                "Received phase in Local %s, Expected output phase %s, but instead got %s" % (
                    phase_key,
                    expected_cp,
                    actual_cp
            )
            break