from .entity import *
from .consts import *
from .properties import *
from .utils import *

@register_entity("DT_DOTAGamerulesProxy")
class GameInfo(DotaEntity):
  """
  Inherits from :class:`DotaEntity`

  The GameInfo contains the macro state of the game; the stage of the game
  that the tick is in, whether the tick is in day or night, the length of
  the game, etc etc.
  """

  game_time = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_fGameTime")
  """
  The time in seconds of the current tick.
  """

  load_time = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_flGameLoadTime")\
    .apply(FuncTrans(none_or_nonzero))
  """
  The time that the game_state changed to ``loading``.
  """

  draft_start_time = Property("DT_DOTAGamerulesProxy",
                              "DT_DOTAGamerules.m_flHeroPickStateTransitionTime")\
    .apply(FuncTrans(none_or_nonzero))
  """
  The time that the game_state changed to ``draft``.
  """

  pregame_start_time = Property("DT_DOTAGamerulesProxy",
                                "DT_DOTAGamerules.m_flPreGameStartTime")\
    .apply(FuncTrans(none_or_nonzero))
  """
  The time that the game_state changed to ``pregame``.
  """

  game_start_time = Property("DT_DOTAGamerulesProxy",
                             "DT_DOTAGamerules.m_flGameStartTime")\
    .apply(FuncTrans(none_or_nonzero))
  """
  The time that the game_state changed to ``game``.
  """

  game_end_time = Property("DT_DOTAGamerulesProxy",
                           "DT_DOTAGamerules.m_flGameEndTime")\
    .apply(FuncTrans(none_or_nonzero))
  """
  The time that the game_state changed to ``postgame``.
  """

  match_id = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_unMatchID")
  """
  The unique match id, used by the Steam API and stuff (i.e. DotaBUff and
  friends).
  """

  game_state = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_nGameState")\
    .apply(MapTrans(GAME_STATE_VALUES))
  """
  The state of the game. Potential values are:

  * ``"loading"`` - Players are loading into the game
  * ``"draft"`` - The draft state has begun
  * ``"strategy"`` - Unknown
  * ``"pregame"`` - The game has started but creeps have not been
    spawned
  * ``"game"`` - The main game, between the first creep spawn and the
    ancient being destroyed
  * ``"postgame"`` - After the ancient has been destroyed
  * ``"disconnect"`` - Unknown
  """

  game_mode = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_iGameMode")\
    .apply(MapTrans(GAME_MODE_VALUES))
  """
  The mode of the dota game. Possible values are:

  * ``"none"``
  * ``"all pick"``
  * ``"captain's mode"``
  * ``"random draft"``
  * ``"single draft"``
  * ``"all random"``
  * ``"intro"``
  * ``"diretide"``
  * ``"reverse captain's mode"``
  * ``"greeviling"``
  * ``"tutorial"``
  * ``"mid only"``
  * ``"least played"``
  * ``"new player pool"``
  * ``"compendium matchmaking"``
  """

  starting_team = Property("DT_DOTAGamerulesProxy",
                           "DT_DOTAGamerules.m_iStartingTeam")\
    .apply(MapTrans(TEAM_VALUES))
  """
  The team that begins the draft.
  """

  pausing_team = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_iPauseTeam")\
    .apply(MapTrans(TEAM_VALUES))
  """
  The team that is currently pausing. Will be ``None`` if the game is not
  paused, otherwise either ``"radiant"`` or ``"dire"``.
  """

  active_team = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_iActiveTeam")\
    .apply(MapTrans(TEAM_VALUES))
  """
  The team that is currently banning/picking.
  """

  pick_state = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_iHeroPickState")\
    .apply(MapTrans(PICK_VALUES))
  """
  The current pick/ban that is happening. ``None`` if no pick or ban is
  happening. If the :attr:`game_mode` is not ``"captain's mode"``, the
  possible values are:

  * ``"all pick"``
  * ``"single draft"``
  * ``"random draft"``
  * ``"all random"``

  Otherwise, the current pick and ban is returned in a tuple of the type of
  draft action and the index. For example, if the current tick was during
  the 5th ban of a captains mode game, the value of :attr:`pick_state` would
  be ``("ban", 5)``. :attr:`active_team` could then be used to work out who
  is banning. Alternatively, if it was the 2nd pick of the game, it would be
  ``("pick", 2)``.
  """

  game_winner = Property("DT_DOTAGamerulesProxy", "DT_DOTAGamerules.m_iHeroPickState")\
    .apply(MapTrans(WINNER_VALUES))
  """
  The winner of the game.
  """

  @property
  def replay_length(self):
    """
    The length in seconds of the replay.
    """
    return self.stream_binding.demo.file_info.playback_time