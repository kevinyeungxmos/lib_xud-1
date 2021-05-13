#!/usr/bin/env python
# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import Pyxsim 
from Pyxsim import testers
import os
import random
import sys
from usb_clock import Clock
from usb_phy import UsbPhy, USB_DATA_VALID_COUNT
from usb_phy_shim import UsbPhyShim
from usb_phy_utmi import UsbPhyUtmi
from usb_packet import RxPacket
from usb_packet import BusReset
import pytest
import tempfile
import shutil
import re

ARCHITECTURE_CHOICES = ['xs2', 'xs3']
BUSSPEED_CHOICES = ['FS', 'HS']
arch_args = {'arch':'xs3'}
XN_FILES = ["test_xs2.xn", "test_xs3.xn"]
clean_only = False

def copy_common_xn_files(test_dir, path = ".", common_dir = "shared_src", source_dir = "src", xn_files = XN_FILES):
    src_dir = os.path.join(test_dir, source_dir)
    for xn_file in xn_files:
        xn = os.path.join(common_dir, xn_file)
        shutil.copy(xn, src_dir)

def delete_test_specific_xn_files(test_dir, path = ".", source_dir = "src", xn_files = XN_FILES):
    src_dir = os.path.join(test_dir, source_dir)
    for xn_file in xn_files:
        xn = os.path.join(src_dir, xn_file)
        os.remove(xn)

def create_if_needed(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def get_usb_clk_phy(verbose=True, test_ctrl=None, do_timeout=True,
                       complete_fn=None, expect_loopback=False,
                       dut_exit_time=350000, arch='xs2'):

    if arch=='xs2':
        clk = Clock('XS1_USB_CLK', Clock.CLK_60MHz)
        phy = UsbPhyUtmi('XS1_USB_RXD',
                         'XS1_USB_RXA', #rxa
                         'XS1_USB_RXV', #rxv
                         'XS1_USB_RXE', #rxe
                         'tile[0]:XS1_PORT_8A', #txd
                         'tile[0]:XS1_PORT_1K', #txv
                         'tile[0]:XS1_PORT_1H', #txrdy
                         'XS1_USB_LS0', 
                         'XS1_USB_LS1',
                         clk,
                         verbose=verbose, test_ctrl=test_ctrl,
                         do_timeout=do_timeout, complete_fn=complete_fn,
                         expect_loopback=expect_loopback,
                         dut_exit_time=dut_exit_time)
 
    elif arch=='xs3':
        clk = Clock('XS1_USB_CLK', Clock.CLK_60MHz)
        phy = UsbPhyUtmi('XS1_USB_RXD',
                         'XS1_USB_RXA', #rxa
                         'XS1_USB_RXV', #rxv
                         'XS1_USB_RXE', #rxe
                         'tile[0]:XS1_PORT_8A', #txd
                         'tile[0]:XS1_PORT_1K', #txv
                         'tile[0]:XS1_PORT_1H', #txrdy
                         'XS1_USB_LS0', 
                         'XS1_USB_LS1',
                         clk,
                         verbose=verbose, test_ctrl=test_ctrl,
                         do_timeout=do_timeout, complete_fn=complete_fn,
                         expect_loopback=expect_loopback,
                         dut_exit_time=dut_exit_time)

    else:
        raise ValueError("Invalid architecture: " + arch)
        
    return (clk, phy)

def run_on_simulator(xe, simthreads, **kwargs):
    for k in ['do_xe_prebuild', 'build_env', 'clean_before_build']:
        if k in kwargs:
            kwargs.pop(k)
    return Pyxsim.run_with_pyxsim(xe, simthreads, **kwargs)

def run_on(**kwargs):

    for name,value in kwargs.items():
        arg_value = arch_args.get(name)
        if arg_value is not None and value != arg_value:
            return False

    return True

def RunUsbTest(test_fn):
   
    tester_list = []
    testname,extension = os.path.splitext(os.path.basename(__file__))
    seed = random.randint(0, sys.maxsize)

    data_valid_count = {'FS': 39, "HS": 0}

    (fd, fname) = tempfile.mkstemp()
    old_std = os.fdopen(os.dup(sys.stdout.fileno()), "w")
    sys.stdout = os.fdopen(fd, "w")
    std_reader = open(fname, "r")

    for _arch in ARCHITECTURE_CHOICES:
        for _busspeed in BUSSPEED_CHOICES:
            if run_on(arch=_arch):
                if run_on(busspeed=_busspeed):
                    (clk_60, usb_phy) = get_usb_clk_phy(verbose=False, arch=_arch)
                    tester_list.extend(test_fn(_arch, clk_60, usb_phy, USB_DATA_VALID_COUNT[_busspeed], _busspeed, seed))

    captured = std_reader.read()
    sys.stdout = old_std
    caps = captured.split("\n")
    return Pyxsim.run_tester(caps,tester_list)

def do_usb_test(arch, clk, phy, usb_speed, sessions, test_file, seed,
               level='nightly', extra_tasks=[], verbose=False):

    """ Shared test code for all RX tests using the test_rx application.
    """
    testname,extension = os.path.splitext(os.path.basename(test_file))
    tester_list = []

    binary = '{testname}/bin/{arch}/{testname}_{arch}.xe'.format(testname=testname, arch=arch)
    copy_common_xn_files(testname)
    build_success, build_output = Pyxsim._build(binary)
    # print(binary)

    assert len(sessions) == 1, "Multiple sessions not yet supported"
    if build_success:
        for session in sessions:
       
            events = session.events
            phy.events = session.events

            expect_folder = create_if_needed("expect")
            expect_filename = '{folder}/{test}_{arch}.expect'.format(
                folder=expect_folder, test=testname, phy=phy.name, clk=clk.get_name(), arch=arch)

            create_expect(arch, session.events, expect_filename, verbose=verbose)

            tester = testers.ComparisonTester(open(expect_filename),
                                          'lib_xud', 'xud_sim_tests', testname,
                                         {'clk':clk.get_name(), 'arch':arch, 'speed':usb_speed})

            tester_list.append(tester)

            simthreads = [clk, phy] + extra_tasks
            run_on_simulator(binary, simthreads)  
        delete_test_specific_xn_files(testname)
        return tester_list
    else:
        delete_test_specific_xn_files(testname)
        return False

def create_expect(arch, events, filename, verbose = False):
    
    """ Create the expect file for what packets should be reported by the DUT
    """
    with open(filename, 'w') as f:
        
        packet_offset = 0
        
        if verbose:
            print("EXPECTED OUTPUT:")
        for i, event in enumerate(events):
           
            expect_str = event.expected_output(offset = packet_offset)
            packet_offset += event.event_count
            
            if verbose:
                print(str(expect_str), end=' ') 
            
            f.write(str(expect_str))
        
        f.write("Test done\n")

        if verbose:
            print("Test done\n")

def get_sim_args(testname, clk, phy, arch='xs2'):
    sim_args = []

    if args and args.trace:
        log_folder = create_if_needed("logs")

        filename = "{log}/xsim_trace_{test}_{clk}_{arch}".format(
            log=log_folder, test=testname,
            clk=clk.get_name(), phy=phy.name, arch=arch)

        sim_args += ['--trace-to', '{0}.txt'.format(filename), '--enable-fnop-tracing']

        vcd_args  = '-o {0}.vcd'.format(filename)
        vcd_args += (' -tile tile[0] -ports -ports-detailed -instructions'
                     ' -functions -cycles -clock-blocks -pads -cores')

        sim_args += ['--vcd-tracing', vcd_args]
#        sim_args += ['--xscope', '-offline logs/xscope.xmt']

    return sim_args

def packet_processing_time(phy, data_bytes):
    """ Returns the time it takes the DUT to process a given frame
    """
    return 6000 * phy.clock.get_bit_time()

def choose_small_frame_size(rand):
    """ Choose the size of a frame near the minimum size frame (46 data bytes)
    """
    return rand.randint(46, 54)

def move_to_next_valid_packet(phy):
    while (phy.expect_packet_index < phy.num_expected_packets and
           phy.expected_packets[phy.expect_packet_index].dropped):
        phy.expect_packet_index += 1

def check_received_packet(packet, phy):
    if phy.expected_packets is None:
        return

    move_to_next_valid_packet(phy)

    if phy.expect_packet_index < phy.num_expected_packets:
        expected = phy.expected_packets[phy.expect_packet_index]
        if packet != expected:
            print("ERROR: packet {n} does not match expected packet".format(
                n=phy.expect_packet_index))

            print("Received:")
            sys.stdout.write(packet.dump())
            print("Expected:")
            sys.stdout.write(expected.dump())

        print("Received packet {} ok".format(phy.expect_packet_index))
        # Skip this packet
        phy.expect_packet_index += 1

        # Skip on past any invalid packets
        move_to_next_valid_packet(phy)

    else:
        print("ERROR: received unexpected packet from DUT")
        print("Received:")
        sys.stdout.write(packet.dump())

    if phy.expect_packet_index >= phy.num_expected_packets:
        print("Test done")
        phy.xsi.terminate()

