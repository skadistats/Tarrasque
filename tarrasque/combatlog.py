from . import gameevents
from .properties import *
from .consts import *

@gameevents.register_event("dota_combatlog")
class CombatLogMessage(gameevents.GameEvent):
  """
  A message in the combat log.
  """

  type = Property("type").apply(MapTrans(COMBAT_LOG_TYPES))

  target_name = Property("targetname")\
    .apply(StringTableTrans("CombatLogNames"))\
    .apply(FuncTrans(lambda n: n[0]))