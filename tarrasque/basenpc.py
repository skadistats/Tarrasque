from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTA_BaseNPC")
class BaseNPC(DotaEntity):
  position = PositionProperty("DT_DOTA_BaseNPC")

  life_state = Property("DT_DOTA_BaseNPC", "m_lifeState")\
    .apply(MapTrans(LIFE_STATE_VALUES))

  level = Property("DT_DOTA_BaseNPC", "m_iCurrentLevel")

  health = Property("DT_DOTA_BaseNPC", "m_iHealth")

  max_health = Property("DT_DOTA_BaseNPC", "m_iMaxHealth")

  health_regen = Property("DT_DOTA_BaseNPC", "m_flHealthThinkRegen")

  mana = Property("DT_DOTA_BaseNPC", "m_flMana")

  max_mana = Property("DT_DOTA_BaseNPC", "m_flMaxMana")

  mana_regen = Property("DT_DOTA_BaseNPC", "m_flManaThinkRegen")

  abilities = ArrayProperty("DT_DOTA_BaseNPC", "m_hAbilities", array_length=16)\
    .filter(lambda h: h != NEGATIVE)\
    .map(EntityTrans())

  @property
  def is_alive(self):
    return self.life_state == "alive"
