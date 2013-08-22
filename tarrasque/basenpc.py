from .entity import *
from .properties import *

@register_entity("DT_DOTA_BaseNPC")
class BaseNPC(DotaEntity):
  position = PositionProperty("DT_DOTA_BaseNPC")