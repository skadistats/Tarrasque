import unittest

import tarrasque

from .utils import *

class StreamBindingMovementTestCase(unittest.TestCase):
    REPLAY_FILE = "./demo/PL.dem"

    @classmethod
    def setUpClass(cls):
        cls.replay = tarrasque.StreamBinding.from_file(cls.REPLAY_FILE)

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

    def test_go_to_state_change(self):
        states = ["pregame", "game", "postgame"]

        for state_name in states:
            self.replay.go_to_tick(state_name)
            change_tick = self.replay.tick
            eq_(self.replay.info.game_state, state_name)
            while self.replay.tick == change_tick:
                self.replay.go_to_tick(self.replay.tick - 10)

            neq_(self.replay.info.game_state, state_name)

class StreamBindingConstantTestCase(unittest.TestCase):
    REPLAY_FILE = "./demo/PL.dem"

    def setUp(self):
        self.replay = tarrasque.StreamBinding.from_file(self.REPLAY_FILE,
                                                        start_tick="game")

    def test_number_of_players(self):
        eq_(len(self.replay.players), 10)

    def test_no_spectators_in_players(self):
        for player in self.replay.players:
            in_(player.team, ["radiant", "dire"])

    def test_player_heroes(self):
        for player in self.replay.players:
            neq_(player.hero, None)
