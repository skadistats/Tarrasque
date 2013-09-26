from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTA_BaseNPC")
class BaseNPC(DotaEntity):
  """
  A base class for all NPCs, even ones controllable by players.
  """

  position = PositionProperty("DT_DOTA_BaseNPC")
  """
  The (x, y) position of the NPC in Dota2 map coordinates
  """

  life_state = Property("DT_DOTA_BaseNPC", "m_lifeState")\
    .apply(MapTrans(LIFE_STATE_VALUES))
  """
  The state of the NPC's life (unsurprisingly). Possible values are:

  * ``"alive"`` - The hero is alive
  * ``"dying"`` - The hero is in their death animation
  * ``"dead"`` - The hero is dead
  * ``"respawnable"`` - The hero can be respawned
  * ``"discardbody"`` - The hero's body can be discarded

  ``"respawnable"`` and ``"discardbody"`` shouldn't occur in a Dota2 replay
  """

  level = Property("DT_DOTA_BaseNPC", "m_iCurrentLevel")
  """
  The NPC's level. See :attr:`Hero.ability_points` for unspent level up
  ability points.
  """

  health = Property("DT_DOTA_BaseNPC", "m_iHealth")
  """
  The NPC's current HP.
  """

  max_health = Property("DT_DOTA_BaseNPC", "m_iMaxHealth")
  """
  The NPC's maximum HP.
  """

  health_regen = Property("DT_DOTA_BaseNPC", "m_flHealthThinkRegen")
  """
  The NPC's health regen per second.
  """

  mana = Property("DT_DOTA_BaseNPC", "m_flMana")
  """
  The NPC's current mana.
  """

  max_mana = Property("DT_DOTA_BaseNPC", "m_flMaxMana")
  """
  The NPC's maximum mana.
  """

  mana_regen = Property("DT_DOTA_BaseNPC", "m_flManaThinkRegen")
  """
  The NPC's mana regen per second.
  """

  abilities = ArrayProperty("DT_DOTA_BaseNPC", "m_hAbilities", array_length=16)\
    .filter(lambda h: h != NEGATIVE)\
    .map(EntityTrans())
  """
  A list of the NPC's abilities.
  """
  
  inventory = ArrayProperty('DT_DOTA_UnitInventory', 'm_hItems', array_length = 14)\
    .filter(lambda h: h != NEGATIVE)\
    .map(EntityTrans())
  """
  A list of the NPC's items.
  """
  
  @property
  def is_alive(self):
    """
    A boolean to test if the NPC is alive or not.
    """
    return self.life_state == "alive"
