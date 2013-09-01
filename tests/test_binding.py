import unittest

import tarrasque

class StreamBindingTestCase(unittest.TestCase):
  REPLAY_FILE = "./demo/PL.dem"

  def setUp(self):
    self.replay = tarrasque.StreamBinding.from_file(self.REPLAY_FILE)

  def test_go_to_time(self):
    self.replay.go_to_time(3 * 60 + 50)
    assert int(self.replay.info.game_time) == 3 * 60 + 50

  def test_go_to_tick(self):
    self.replay.go_to_tick(2000)
    assert self.replay.tick >= 2000 and self.replay.tick <= 2002