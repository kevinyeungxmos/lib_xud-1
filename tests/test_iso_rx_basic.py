# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from usb_session import UsbSession
from usb_transaction import UsbTransaction
import pytest
from conftest import PARAMS, test_RunUsbSession  # noqa F401


@pytest.fixture
def test_session(ep, address, bus_speed):

    start_length = 10
    end_length = start_length + 5

    session = UsbSession(
        bus_speed=bus_speed, run_enumeration=False, device_address=address
    )

    for pktLength in range(start_length, end_length):
        session.add_event(
            UsbTransaction(
                session,
                deviceAddress=address,
                endpointNumber=ep,
                endpointType="ISO",
                direction="OUT",
                dataLength=pktLength,
            )
        )

    return session
