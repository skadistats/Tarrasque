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
  """
  The name of the entity that was targeted in the event. Note that this is not
  the dt name or "pretty" name, this is the :attr:`DotaEntity.raw_name`. So for
  a message where Shadow Field is being attacked, this would be
  ``"dt_dota_nevermore"``.
  """