import unittest

import tarrasque

from .utils import *

class PlayerTestCase(unittest.TestCase):
  REPLAY_FILE = "./demo/PL.dem"

  @classmethod
  def setUpClass(cls):
    cls.replay = tarrasque.StreamBinding.from_file(cls.REPLAY_FILE,
                                                   start_tick="game")

  def test_players_have_names(self):
    for player in self.replay.players:
      neq_(player.name, None)

  def test_player_have_hero(self):
    for player in self.replay.players:
      neq_(player.hero, None)