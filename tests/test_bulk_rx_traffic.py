#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import random
from  usb_packet import *
import usb_packet
from usb_clock import Clock
from helpers import do_usb_test, get_usb_clk_phy, runall_rx
from usb_clock import Clock
from usb_phy_utmi import UsbPhyUtmi
import Pyxsim
import pytest
import os

def do_test(arch, clk, phy, data_valid_count, usb_speed, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 1
    address = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    pid = PID_DATA0;

    trafficAddress1 = 0;
    trafficAddress2 = 127;

    trafficEp1 = 15;
    trafficEp2 = 0;

    for pktlength in range(10, 20):

        AppendOutToken(packets, trafficEp1, trafficAddress1, data_valid_count=data_valid_count, inter_pkt_gap=500)
        packets.append(TxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 

        AppendOutToken(packets, ep, address, data_valid_count=data_valid_count, inter_pkt_gap=500)
        packets.append(TxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 
        packets.append(RxHandshakePacket(data_valid_count=data_valid_count))
  
        AppendOutToken(packets, trafficEp2, trafficAddress2, data_valid_count=data_valid_count, inter_pkt_gap=500)
        packets.append(TxDataPacket(rand, data_start_val=dataval, data_valid_count=data_valid_count, length=pktlength, pid=pid)) 

        if(pid == usb_packet.PID_DATA1):
            pid = usb_packet.PID_DATA0;
        else:
            pid = usb_packet.PID_DATA1;

        dataval += pktlength

        trafficEp1 = trafficEp1 - 1
        if(trafficEp1 < 0):
            trafficEp1 = 15
        
        trafficEp2 + trafficEp2 + 1
        if(trafficEp1 > 15):
            trafficEp1 = 0

    tester = do_usb_test(arch, clk, phy, usb_speed, packets, __file__, seed, level='smoke', extra_tasks=[])

    return tester

def test_bulk_rx_traffic():
    random.seed(1)
    for result in runall_rx(do_test):
        assert result