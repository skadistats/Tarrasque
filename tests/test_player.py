import unittest

import tarrasque

from .utils import *

class PlayerTestCase(unittest.TestCase):
    REPLAY_FILE = "./tests/fixtures/PL.dem"

    @classmethod
    def setUpClass(cls):
        cls.replay = tarrasque.StreamBinding.from_file(cls.REPLAY_FILE,
                                                       start=10000)
        cls.player = cls.replay.players[4]

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

    def test_have_name(self):
        eq_(self.player.name, "Gyozmo")

    def test_have_hero(self):
        neq_(self.player.hero, None)

    def test_reliable_gold(self):
        eq_(self.player.reliable_gold, 0)

    def test_unreliable_gold(self):
        eq_(self.player.unreliable_gold, 154)

    def test_earned_gold(self):
        eq_(self.player.earned_gold, 150)

    def test_steam_id(self):
        eq_(self.player.steam_id, 2865091096608769)

    def test_team(self):
        eq_(self.player.team, "radiant")

    def test_last_hits(self):
        eq_(self.player.last_hits, 1)

    def test_denies(self):
        eq_(self.player.denies, 0)

    def test_kills(self):
        eq_(self.player.kills, 0)

    def test_deaths(self):
        eq_(self.player.deaths, 0)

    def test_assists(self):
        eq_(self.player.assists, 0)

    def test_streak(self):
        eq_(self.player.streak, 0)

    def test_buyback_cooldown_time(self):
        eq_(self.player.buyback_cooldown_time, 0.0)

    def test_last_buyback_time(self):
        eq_(self.player.last_buyback_time, 0)

    def test_has_buyback(self):
        eq_(self.player.has_buyback, True)

    def test_total_gold(self):
        eq_(self.player.total_gold, 154)
