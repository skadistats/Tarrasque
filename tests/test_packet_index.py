import unittest

import importlib
import os

import skadi.io.demo

from tarrasque import packet_index

from .utils import *

def test_bin_search():
    def i_f(v):
        if v == 55:
            return 0
        elif v < 55:
            return -1
        else:
            return 1
        assert False

    eq_(55, packet_index._bin_search(range(100), i_f))
    eq_(155, packet_index._bin_search(range(-100, 100), i_f))

class PacketIndexTestCase(unittest.TestCase):
    REPLAY_FILE = "./tests/fixtures/PL.dem"

    def setUp(self):
        self.demo_file = open(self.REPLAY_FILE, "rb")
        self.demoio = skadi.io.demo.mk(self.demo_file)
        self.demoio.bootstrap()

    def test_from_demoio(self):
        pi = packet_index.PacketIndex.from_demoio(self.demoio)
        eq_(len(pi.packets), 31463)
        eq_(len(pi.full_indexes), 35)

    def test_packets_for_tick(self):
        pi = packet_index.PacketIndex.from_demoio(self.demoio)
        fps, ps = pi.packets_for_tick(1050)
        eq_(len(fps), 1)
        eq_(len(ps), 524)
