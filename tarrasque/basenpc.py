from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTA_BaseNPC")
class BaseNPC(DotaEntity):
  position = PositionProperty("DT_DOTA_BaseNPC")

  life_state = Property("DT_DOTA_BaseNPC", "i_mLifeState")\
    .value_map(LIFE_STATE_VALUES)

  @property
  def is_alive(self):
    return self.life_state == "alive"