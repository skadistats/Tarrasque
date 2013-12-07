import unittest

import importlib
import os

import skadi.io.demo

from tarrasque import packet_index

from .utils import *

class PacketIndexTestCase(unittest.TestCase):
    REPLAY_FILE = "./demo/PL.dem"

    def setUp(self):
        self.demo_file = open(self.REPLAY_FILE, "rb")
        self.demoio = skadi.io.demo.mk(self.demo_file)
        self.demoio.bootstrap()

    def test_from_demoio(self):
        pi = packet_index.PacketIndex.from_demoio(self.demoio)
        eq_(len(pi.packets), 31463)
        eq_(len(pi.full_indexes), 35)