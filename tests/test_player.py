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

  def test_players_last_hits(self):
    for player in self.replay.players:
      gt_(player.last_hits, -1)

  def test_players_denies(self):
    for player in self.replay.players:
      gt_(player.denies, -1)

  def test_players_kills(self):
    for player in self.replay.players:
      gt_(player.kills, -1)

  def test_players_deaths(self):
    for player in self.replay.players:
      gt_(player.deaths, -1)

  def test_players_assists(self):
    for player in self.replay.players:
      gt_(player.assists, -1)

  def test_players_streak(self):
    for player in self.replay.players:
      gt_(player.streak, -1)

  def test_players_buyback_cooldown_time(self):
    for player in self.replay.players:
      gt_(player.buyback_cooldown_time, -1)

  def test_players_last_buyback_time(self):
    for player in self.replay.players:
      gt_(player.last_buyback_time, -1)

  def test_players_has_buyback(self):
    for player in self.replay.players:
      eq_(player.has_buyback, True)

  def test_players_total_gold(self):
    for player in self.replay.players:
      eq_(player.total_gold, player.unreliable_gold + player.reliable_gold)