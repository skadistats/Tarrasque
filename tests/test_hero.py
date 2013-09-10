import unittest

import tarrasque

from .utils import *

class HeroTestCase(unittest.TestCase):
  REPLAY_FILE = "./demo/PL.dem"

  @classmethod
  def setUpClass(cls):
    cls.replay = tarrasque.StreamBinding.from_file(cls.REPLAY_FILE,
                                                   start_tick=10000)
    cls.heroes = [p.hero for p in cls.replay.players]
    cls.player = cls.replay.players[0]
    cls.hero = cls.player.hero

  def test_heroes_name(self):
    for hero in self.heroes:
      neq_(hero.name, None)

  def test_heroes_xp(self):
    for hero in self.heroes:
      gt_(hero.xp, 0)

  def test_heroes_respawn_time(self):
    for hero in self.heroes:
      neq_(hero.respawn_time, None)

  def test_heroes_ability_points(self):
    for hero in self.heroes:
      neq_(hero.ability_points, None)

  def test_heroes_natural_strength(self):
    for hero in self.heroes:
      gt_(hero.natural_strength, 0)

  def test_heroes_natural_agility(self):
    for hero in self.heroes:
      gt_(hero.natural_agility, 0)

  def test_heroes_natural_intelligence(self):
    for hero in self.heroes:
      gt_(hero.natural_intelligence, 0)

  def test_heroes_strength(self):
    for hero in self.heroes:
      gteq_(hero.strength, hero.natural_strength)

  def test_heroes_agility(self):
    for hero in self.heroes:
      gteq_(hero.agility, hero.natural_agility)

  def test_heroes_intelligence(self):
    for hero in self.heroes:
      gteq_(hero.intelligence, hero.natural_intelligence)

  def test_heroes_recent_damage(self):
    for hero in self.heroes:
      gteq_(hero.recent_damage, 0)

  def test_heroes_spawned_at(self):
    for hero in self.heroes:
      gteq_(hero.spawned_at, 1 * 60 + 30)

  def test_heroes_replicating_hero(self):
    for hero in self.heroes:
      eq_(hero.replicating_hero, None)

  def test_heroes_player(self):
    for player in self.replay.players:
      eq_(player.hero.player.name, player.name)
      eq_(player.hero.player, player)