#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import random
from  usb_packet import *
import usb_packet
from usb_clock import Clock
from helpers import do_usb_test, get_usb_clk_phy
from usb_clock import Clock
from usb_phy_shim import UsbPhyShim
from usb_phy_utmi import UsbPhyUtmi
import pytest
import os

ARCHITECTURE_CHOICES = ['xs2', 'xs3']
BUSSPEED_CHOICES = ['FS', 'HS']
args = {'arch':'xs3'}
tester_list = []


def do_test(arch, tx_clk, tx_phy, data_valid_count, usb_speed, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 1
    address = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    pid = PID_DATA0;

    pktlength = 10

    for i in range(0, 4):

        if(i == 2):
            AppendInToken(packets, ep, address, data_valid_count=data_valid_count, inter_pkt_gap=4000)
            packets.append(RxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 
            # Missing ACK - simulate CRC fail at host

        AppendInToken(packets, ep, address, data_valid_count=data_valid_count, inter_pkt_gap=4000)
        packets.append(RxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 
        packets.append(TxHandshakePacket(data_valid_count=data_valid_count))
        
        if(pid == usb_packet.PID_DATA1):
            pid = usb_packet.PID_DATA0;
        else:
            pid = usb_packet.PID_DATA1;

        dataval += pktlength
        pktlength += 1

    # Note, quite big gap to allow checking.
    tester = do_usb_test(arch, tx_clk, tx_phy, usb_speed, packets, __file__, seed,
               level='smoke', extra_tasks=[])

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
    separate_point = [index for index, element in enumerate(caps) if element.strip() == "Test done"]
    result = []
    if len(separate_point) > 1:
        i = 0
        start = 0
        stop = 0
        while(i<len(separate_point)):
            if i == 0:
                stop = separate_point[i]+1
            else:
                start = separate_point[i-1]+1
                stop = separate_point[i]+1
            re_cap = caps[start:stop]
            result.append(tester_list[i]._run(re_cap)) 
            i += 1
    else:
        result.append(tester_list[0]._run(caps[:separate_point[0]+1])) 
    return result


def test_bulk_tx_noack(runall_rx):
    random.seed(1)
    for result in runall_rx:
        assert result
