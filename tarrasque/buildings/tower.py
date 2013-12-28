from .building import *

@register_entity("DT_DOTA_BaseNPC_Tower")
class Tower(Building):
  """
  Inherits from :class:`Building`.

  Represents a Tower in the game.
  """

  lane = Property("DT_BaseEntity", "m_iName")\
        .apply(FuncTrans(lambda n: re.findall('(?<=tower)([1-4])\_([a-z]*)', n)[0][1] if n else None))
  """
  Lane of the tower. ``"bot"``, ``"mid"`` or ``"top"``.
  """

  tier = Property("DT_BaseEntity", "m_iName")\
        .apply(FuncTrans(lambda n: re.findall('(?<=tower)([1-4])\_([a-z]*)', n)[0][0] if n else None))
  """
  Tier of the tower, 1-4.
  """