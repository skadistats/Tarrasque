from .entity import *
from .consts import *
from .properties import *

class PlayerResourceProperty(ArrayProperty):
  def get_property(self, entity):
    index = getattr(entity, self.index_var)
    if index == NEGATIVE:
      return None

    ehandle, properties = entity.world.find_by_dt("DT_DOTA_PlayerResource")

    # Work around a bug in skadi
    key = (self.property_key[1], "%04d" % index)
    return properties[key]

@register_entity("DT_DOTAPlayer")
class Player(DotaEntity):
  index = Property("DT_DOTAPlayer", "m_iPlayerID")

  hero = ArrayProperty(
    # The key that the item can be found at
    "DT_DOTA_PlayerResource", "m_hSelectedHero",
    # Not shown, default argument of "index"; the variable to find the
    # array index in
  ).is_ehandle(
    # Members of the Player class we want passed to the target class's
    # __init__
    passed={"self": "player"}
  )

  reliable_gold = PlayerResourceProperty(
    "DT_DOTA_PlayerResource", "m_iReliableGold")

  unreliable_gold = PlayerResourceProperty(
    "DT_DOTA_PlayerResource", "m_iUnreliableGold")

  name = PlayerResourceProperty(
    "DT_DOTA_PlayerResource", "m_iszPlayerNames")

  team = PlayerResourceProperty(
    "DT_DOTA_PlayerResource", "m_iPlayerTeams").is_team()

  @property
  def total_gold(self):
    return self.reliable_gold + self.unreliable_gold

  def __str__(self):
    return "Player({}, {})".format(self.player_index, self.name)
