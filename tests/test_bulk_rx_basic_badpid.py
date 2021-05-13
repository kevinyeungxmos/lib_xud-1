#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import Pyxsim
from  usb_packet import *
import usb_packet
from helpers import do_usb_test, RunUsbTest
from usb_session import UsbSession
from usb_transaction import UsbTransaction
import pytest

# Tests out of seq (but valid.. ) data PID
def do_test(arch, clk, phy, data_valid_count, usb_speed, seed, verbose=False):

    address = 1
    ep = 1

    session = UsbSession(bus_speed=usb_speed, run_enumeration = False, device_address=address)

    # The large inter-frame gap is to give the DUT time to print its output
    interEventDelay = 500
   
    # Valid OUT transaction
    session.add_event(UsbTransaction(session, deviceAddress=address, endpointNumber=ep, endpointType="BULK", direction= "OUT", dataLength=10, interEventDelay=interEventDelay))
    
    # Pretend the ACK went missing on the way to host. Re-send same packet. xCORE should ACK but throw pkt away
    session.add_event(UsbTransaction(session, deviceAddress = address, endpointNumber=ep, endpointType="BULK", direction= "OUT", dataLength=11, interEventDelay=interEventDelay, 
        resend=True))
    
    # Send some valid OUT transactions
    session.add_event(UsbTransaction(session, deviceAddress=address, endpointNumber=ep, endpointType="BULK", direction= "OUT", dataLength=12, interEventDelay=interEventDelay))
    session.add_event(UsbTransaction(session, deviceAddress=address, endpointNumber=ep, endpointType="BULK", direction= "OUT", dataLength=13, interEventDelay=interEventDelay))
    session.add_event(UsbTransaction(session, deviceAddress=address, endpointNumber=ep, endpointType="BULK", direction= "OUT", dataLength=14, interEventDelay=interEventDelay))

    return do_usb_test(arch, clk, phy, usb_speed, [session], __file__, seed, level='smoke', extra_tasks=[], verbose=verbose)

def test_bulk_rx_basic_badpid():
    for result in RunUsbTest(do_test):
        assert result
