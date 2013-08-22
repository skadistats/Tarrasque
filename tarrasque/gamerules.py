from .entity import *
from .consts import *
from .properties import *

@register_entity("DT_DOTAGamerulesProxy")
class GameRules(DotaEntity):
  game_state = Property("DT_DOTAGamerules", "m_nGameState")\
    .value_map(GAME_STATE_VALUES)