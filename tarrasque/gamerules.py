from .entity import *
from .consts import *
from .properties import *
from .utils import *

@register_entity("DT_DOTAGamerulesProxy")
class GameRules(DotaEntity):
  game_time = Property("DT_DOTAGamerules", "m_fGameTime")

  load_time = Property("DT_DOTAGamerules", "m_flGameLoadTime")\
    .apply(FuncTrans(none_or_nonzero))

  draft_start_time = Property("DT_DOTAGamerules", "m_flHeroPickStateTransitionTime")\
    .apply(FuncTrans(none_or_nonzero))

  pregame_start_time = Property("DT_DOTAGamerules", "m_flPreGameStartTime")\
    .apply(FuncTrans(none_or_nonzero))

  game_start_time = Property("DT_DOTAGamerules", "m_flGameStartTime")\
    .apply(FuncTrans(none_or_nonzero))

  game_end_time = Property("DT_DOTAGamerules", "m_flGameEndTime")\
    .apply(FuncTrans(none_or_nonzero))

  match_id = Property("DT_DOTAGamerules", "m_unMatchID")

  game_state = Property("DT_DOTAGamerules", "m_nGameState")\
    .apply(MapTrans(GAME_STATE_VALUES))

  game_mode = Property("DT_DOTAGamerules", "m_iGameMode")\
    .apply(MapTrans(GAME_MODE_VALUES))

  starting_team = Property("DT_DOTAGamerules", "m_iStartingTeam")\
    .apply(MapTrans(TEAM_VALUES))

  pausing_team = Property("DT_DOTAGamerules", "m_iPauseTeam")\
    .apply(MapTrans(TEAM_VALUES))

  active_team = Property("DT_DOTAGamerules", "m_iActiveTeam")\
    .apply(MapTrans(TEAM_VALUES))

  pick_state = Property("DT_DOTAGamerules", "m_iHeroPickState")\
    .apply(MapTrans(PICK_VALUES))

  game_winner = Property("DT_DOTAGamerules", "m_iHeroPickState")\
    .apply(MapTrans(WINNER_VALUES))
