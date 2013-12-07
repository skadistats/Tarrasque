import unittest

import importlib
import os

from protobuf.impl import demo_pb2 as pb_d
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
        tick = 1050

        pi = packet_index.PacketIndex.from_demoio(self.demoio)
        fps, ps = pi.packets_for_tick(tick)
        eq_(len(fps), 1)
        eq_(len(ps), 524)
        eq_((ps[-1] if ps else fps[-1])[0].tick, tick)

class PacketIterTestCase(unittest.TestCase):
    REPLAY_FILE = "./tests/fixtures/PL.dem"

    def setUp(self):
        self.demo_file = open(self.REPLAY_FILE, "rb")
        self.demoio = skadi.io.demo.mk(self.demo_file)
        self.demoio.bootstrap()
        self.packet_index = packet_index.PacketIndex.from_demoio(self.demoio)

    def test_create_packet_iter(self):
        i = iter(self.packet_index)

    def test_forward(self):
        i = iter(self.packet_index)
        i.move(1050)
        t1 = i.next()
        t2 = i.next()
        gt_(t2[0].tick, t1[0].tick)

    def test_backwards(self):
        i = iter(self.packet_index)
        i.move(1050)
        t1 = i.prev()
        t2 = i.prev()
        gt_(t1[0].tick, t2[0].tick)

    def test_move(self):
        i = iter(self.packet_index)
        j = iter(self.packet_index)
        i.move(1050)
        j.move(1050)
        eq_(i.current[0].tick, j.current[0].tick)

        eq_(i.next()[0].tick, j.next()[0].tick)

        i.move(2050)
        old_p = i.current
        i.move(2050)
        eq_(old_p, i.current)

    def test_full_ticks(self):
        i = iter(self.packet_index)
        i.move(2050)
        p1 = i.next_full()
        p2 = i.next_full()
        gt_(p2[0].tick, p1[0].tick)
        eq_(p1[0].tick, i.prev_full()[0].tick)

        eq_(p1[0].kind, pb_d.DEM_FullPacket)
        eq_(p2[0].kind, pb_d.DEM_FullPacket)