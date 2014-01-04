from .building import *

@register_entity("DT_DOTA_BaseNPC_Barracks")
class Barrack(Building):
  """
  Inherits from :class:`Building`.

  Represents a Barrack in the game.
  """
  lane = Property("DT_BaseEntity", "m_iName")\
        .apply(FuncTrans(lambda n: re.findall('(?<=rax\_)([a-z]*)\_([a-z]*)', n)[0][1] if n else None))
  """
  Lane of the barracks. ``"bot"``, ``"mid"`` or ``"top"``.
  """

  type = Property("DT_BaseEntity", "m_iName")\
        .apply(FuncTrans(lambda n: re.findall('(?<=rax\_)([a-z]*)\_([a-z]*)', n)[0][0] if n else None))
  """
  Type of the barracks, ``"melee"`` or ``"range"``.
  """