#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from usb_packet import *
import usb_packet
from helpers import do_usb_test, RunUsbTest
from usb_session import UsbSession
from usb_transaction import UsbTransaction
import pytest
from conftest import PARAMS


def gen_test_session(ep, address, usb_speed):

    if usb_speed == "FS":
        pytest.xfail("Known failure at FS")

    address = 1
    pktLength = 10

    session = UsbSession(
        bus_speed=usb_speed, run_enumeration=False, device_address=address
    )

    ep_ctrl = 2
    ep = 1

    # Expect test EP's to be halted
    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
            halted=True,
        )
    )

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
            halted=True,
        )
    )

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="IN",
            halted=True,
        )
    )

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="IN",
            halted=True,
        )
    )

    # Valid transaction to another EP informing test code to clear stall
    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep_ctrl,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
        )
    )

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
            interEventDelay=1000,
        )
    )

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="IN",
            dataLength=pktLength,
        )
    )

    return session


def test_stall_basic(test_arch, test_ep, test_address, test_bus_speed):

    for result in RunUsbTest(
        gen_test_session, test_arch, test_ep, test_address, test_bus_speed, __file__
    ):
        assert result
