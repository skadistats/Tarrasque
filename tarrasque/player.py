from .entity import *
from .consts import *

class Player(DotaEntity):
  def __init__(self, index, *args, **kwargs):
    self.index = index
    DotaEntity.__init__(self, *args, **kwargs)

  hero = ArrayProperty(
    # The key that the item can be found at
    "DT_DOTA_PlayerResource", "m_hSelectedHero",
    # Not shown, default argument of "index"; the variable to find the
    # array index in
  ).targets(
    # The "path" to the target class
    "tarrasque.hero.Hero",
    passed={"self": "player"}
  )

  reliable_gold = ArrayProperty("DT_DOTA_PlayerResource", "m_iReliableGold")

  unreliable_gold = ArrayProperty("DT_DOTA_PlayerResource", "m_iUnreliableGold")

  name = ArrayProperty("DT_DOTA_PlayerResource", "m_iszPlayerNames")

  @property
  def total_gold(self):
    return self.reliable_gold + self.unreliable_gold

  def __str__(self):
    return "Player({}, {})".format(self.player_index, self.name)
