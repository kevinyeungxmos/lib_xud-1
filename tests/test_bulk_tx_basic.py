#!/usr/bin/env python
import random
import xmostest
from  usb_packet import *
from usb_clock import Clock
from helpers import do_usb_test, runall_rx


def do_test(arch, tx_clk, tx_phy, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 2
    address = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    AppendInToken(packets, ep, address)
    packets.append(RxDataPacket(rand, data_start_val=dataval, length=10, pid=0x3)) #DATA0
    packets.append(TxHandshakePacket())

    dataval += 10
    AppendInToken(packets, ep, address, inter_pkt_gap=4000)
    packets.append(RxDataPacket(rand, data_start_val=dataval, length=11, pid=0xb)) #DATA1
    packets.append(TxHandshakePacket())

    dataval += 11
    AppendInToken(packets, ep, address, inter_pkt_gap=4000)
    packets.append(RxDataPacket(rand, data_start_val=dataval, length=12, pid=0x3)) #DATA0
    packets.append(TxHandshakePacket())

    dataval += 12
    AppendInToken(packets, ep, address, inter_pkt_gap=4000)
    packets.append(RxDataPacket(rand, data_start_val=dataval, length=13, pid=0xb)) #DATA1
    packets.append(TxHandshakePacket())

    dataval += 13
    AppendInToken(packets, ep, address, inter_pkt_gap=4000)
    packets.append(RxDataPacket(rand, data_start_val=dataval, length=14, pid=0x3)) #DATA0
    packets.append(TxHandshakePacket())

    # Note, quite big gap to allow checking.
    do_usb_test(arch, tx_clk, tx_phy, packets, __file__, seed,
               level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
