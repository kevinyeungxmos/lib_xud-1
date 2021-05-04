#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import random
from  usb_packet import *
from usb_clock import Clock
from helpers import do_usb_test, get_usb_clk_phy
from usb_clock import Clock
from usb_phy_utmi import UsbPhyUtmi
import Pyxsim
import pytest
import os

ARCHITECTURE_CHOICES = ['xs2', 'xs3']
BUSSPEED_CHOICES = ['FS', 'HS']
args = {'arch':'xs3'}
tester_list = []

def do_test(arch, clk, phy, data_valid_count, usb_speed, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 2
    address = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    # Note, quite big gap to allow checking.
    pid = PID_DATA0;

    for pktlength in range(10, 15):
        AppendOutToken(packets, ep, address, data_valid_count=data_valid_count, inter_pkt_gap=500)
        packets.append(TxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 
        dataval += pktlength

    tester = do_usb_test(arch, clk, phy, usb_speed, packets, __file__, seed, level='smoke', extra_tasks=[])

    return tester

def run_on(**kwargs):

    for name,value in kwargs.items():
        arg_value = args.get(name)
        if arg_value is not None and value != arg_value:
            return False

    return True

@pytest.fixture
def runall_rx(capfd):
    testname,extension = os.path.splitext(os.path.basename(__file__))
    seed = random.randint(0, sys.maxsize)

    data_valid_count = {'FS': 39, "HS": 0}

    for _arch in ARCHITECTURE_CHOICES:
        for _busspeed in BUSSPEED_CHOICES:
            if run_on(arch=_arch):
                if run_on(busspeed=_busspeed):
                    (clk_60, usb_phy) = get_usb_clk_phy(verbose=False, arch=_arch)
                    tester_list.append(do_test(_arch, clk_60, usb_phy, data_valid_count[_busspeed], _busspeed, seed))
    captured = capfd.readouterr()
    caps = captured.out.split("\n")
    
    return Pyxsim.run_tester(caps,tester_list)


def test_iso_rx_basic(runall_rx):
    random.seed(1)
    for result in runall_rx:
        assert result
