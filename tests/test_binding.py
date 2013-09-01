import unittest

import tarrasque

from .utils import *

class StreamBindingMovementTestCase(unittest.TestCase):
  REPLAY_FILE = "./demo/PL.dem"

  def setUp(self):
    self.replay = tarrasque.StreamBinding.from_file(self.REPLAY_FILE)

  def test_go_to_time(self):
    self.replay.go_to_time(3 * 60 + 50)
    eq_(int(self.replay.info.game_time), 3 * 60 + 50)

  def test_go_to_tick(self):
    self.replay.go_to_tick(2000)
    gt_(self.replay.tick, 1999)
    lt_(self.replay.tick, 2003)

  def test_go_to_end(self):
    self.replay.go_to_tick("end")
    ticks_left = self.replay.demo.file_info.playback_ticks - self.replay.tick
    lt_(abs(ticks_left), 3)
    lt_(-1, ticks_left)

class StreamBindingConstantTestCase(unittest.TestCase):
  REPLAY_FILE = "./demo/PL.dem"

  def setUp(self):
    self.replay = tarrasque.StreamBinding.from_file(self.REPLAY_FILE, 20000)

  def test_number_of_players(self):
    eq_(len(self.replay.players), 10)