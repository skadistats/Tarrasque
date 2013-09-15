from .properties import *
from .basenpc import BaseNPC
from .entity import register_entity

@register_entity("DT_DOTA_BaseNPC_Creep_Lane")
class LaneCreep(BaseNPC):
  """
  A lane creep (ranged or melee).
  """

  health_percentage = Property('DT_DOTA_BaseNPC_Creep_Lane',
                               'm_iHealthPercentage')\
    .apply(FuncTrans(lambda h: h / 1.27))

  @property
  def health(self):
    """
    The creep's max health.
    """
    return self.health_percentage * self.max_health / 100