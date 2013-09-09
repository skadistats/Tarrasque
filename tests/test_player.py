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

  def test_players_reliable_gold(self):
    for player in self.replay.players:
      gt_(player.reliable_gold, -1)

  def test_players_unreliable_gold(self):
    for player in self.replay.players:
      gt_(player.unreliable_gold, -1)

  def test_players_earned_gold(self):
    for player in self.replay.players:
      gt_(player.earned_gold, -1)

  def test_players_steam_id(self):
    for player in self.replay.players:
      neq_(player.steam_id, None)

  def test_players_team(self):
    for player in self.replay.players:
      in_(player.team, ["radiant", "dire"])