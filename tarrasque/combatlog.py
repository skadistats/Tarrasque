from . import gameevents
from .properties import *
from .consts import *

@gameevents.register_event("dota_combatlog")
class CombatLogMessage(gameevents.GameEvent):
  """
  A message in the combat log.
  """

  type = Property("type").apply(MapTrans(COMBAT_LOG_TYPES))
  """
  The type of event this message signifies. Options are:

  * ``"damage"`` - One entity is damaging another
  * ``"heal"`` - One entity is healing another
  * ``"modifier added"`` - A modifier is being added to an entity
  * ``"modifier removed"`` - A modifier is being removed from an entity
  * ``"death"`` - An entity has died.
  """

  target_name = Property("targetname")\
    .apply(StringTableTrans("CombatLogNames"))\
    .apply(FuncTrans(lambda n: n[0]))
  """
  The name of the entity that was targeted in the event. Note that this is not
  the dt name or "pretty" name, this is the :attr:`DotaEntity.raw_name`. So for
  a message where Shadow Field is being attacked, this would be
  ``"dt_dota_nevermore"``.
  """

  source_name = Property("sourcename")\
    .apply(StringTableTrans("CombatLogNames"))\
    .apply(FuncTrans(lambda n: n[0]))
  """
  The name of the source of the event.
  """

  attacker_name = Property("sourcename")\
    .apply(StringTableTrans("CombatLogNames"))\
    .apply(FuncTrans(lambda n: n[0]))
  """
  The name of the attacker in the event.
  """

  value = Property("sourcename")\
  """
  The value of the event. Can have various different meanings depending on the
  :attr:`type`.
  """