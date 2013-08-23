from .entity import *
from .consts import *
from .properties import *
from .utils import *

@register_entity("DT_DOTAGamerulesProxy")
class GameRules(DotaEntity):
  game_time = Property("DT_DOTAGamerules", "m_fGameTime")

  load_time = Property("DT_DOTAGamerules", "m_flGameLoadTime")\
              .value_func(none_or_nonzero)

  draft_start_time = Property("DT_DOTAGamerules", "m_flHeroPickStateTransitionTime")\
                     .value_func(none_or_nonzero)

  pregame_start_time = Property("DT_DOTAGamerules", "m_flPreGameStartTime")\
                       .value_func(none_or_nonzero)

  game_start_time = Property("DT_DOTAGamerules", "m_flGameStartTime")\
                    .value_func(none_or_nonzero)

  game_end_time = Property("DT_DOTAGamerules", "m_flGameEndTime")\
                  .value_func(none_or_nonzero)

  match_id = Property("DT_DOTAGamerules", "m_unMatchID")

  game_state = Property("DT_DOTAGamerules", "m_nGameState")\
    .value_map(GAME_STATE_VALUES)

  game_mode = Property("DT_DOTAGamerules", "m_iGameMode")\
              .value_map(GAME_MODE_VALUES)

  starting_team = Property("DT_DOTAGamerules", "m_iStartingTeam")\
                  .value_map(TEAM_VALUES)

  pausing_team = Property("DT_DOTAGamerules", "m_iPauseTeam")\
                 .value_map(TEAM_VALUES)

  active_team = Property("DT_DOTAGamerules", "m_iActiveTeam")\
                .value_map(TEAM_VALUES)

  pick_state = Property("DT_DOTAGamerules", "m_iHeroPickState")\
               .value_map(PICK_VALUES)

  game_winner = Property("DT_DOTAGamerules", "m_iHeroPickState")\
                .value_map(WINNER_VALUES)
