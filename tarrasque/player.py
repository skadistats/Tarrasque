from .entity import *
from .consts import *
from .properties import *

@register_entity("DT_DOTAPlayer")
class Player(DotaEntity):
  """
  Inherits from :class:`DotaEntity`.

  Represents a player in the game. This can be a player who is controlling a
  hero, or a "player" that is spectating.
  """

  index = Property("DT_DOTAPlayer", "m_iPlayerID")\
    .apply(FuncTrans(lambda i: None if i == -1 else i))
  """
  The index of the player in the game. i.e. 0 is the first player on the
  radiant team, 9 is the last on the dire

  This is ``None`` for the undefined player, which should be ignored.
  """

  hero = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_hSelectedHero"))\
    .apply(EntityTrans())
  """
  The :class:`Hero` that the player is playing in the tick. May be ``None``
  if the player has yet to choose a hero. May change when the
  :attr:`~GameInfo.game_state` is ``"pre_game"``, due to players swapping
  their heroes.
  """

  @property
  def reliable_gold(self):
    """
    The player's reliable gold.
    """
    try:
      prop = RemoteProperty("DT_DOTA_Data{}".format(team))\
          .used_by(IndexedProperty("DT_DOTA_DataNonSpectator", "m_iReliableGold")) 
      return prop.get_value(self)
    except (KeyError, IndexError):
      pass

    try:
      prop = RemoteProperty("DT_DOTA_PlayerResource")\
        .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iReliableGold"))
      return prop.get_value(self)
    except (KeyError, IndexError):
      pass

    team = self.team.capitalize()
    dt_class = "DT_{}Data".format(team)
    dt_prop = "m_iReliableGold{}.{:04d}".format(team, self.index)
    prop = RemoteProperty("DT_DOTA_PlayerResource")\
           .used_by(Property(dt_class, dt_prop))
    return prop.get_value(self)

  @property
  def unreliable_gold(self):
    """
    The player's unreliable gold.
    """
    try:
      prop = RemoteProperty("DT_DOTA_Data{}".format(team))\
          .used_by(IndexedProperty("DT_DOTA_DataNonSpectator", "m_iUnreliableGold")) 
      return prop.get_value(self)
    except (KeyError, IndexError):
      pass

    try:
      prop = RemoteProperty("DT_DOTA_PlayerResource")\
        .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iUnreliableGold"))
      return prop.get_value(self)
    except KeyError:
      pass

    team = self.team.capitalize()
    dt_class = "DT_{}Data".format(team)
    dt_prop = "m_iUnreliableGold{}.{:04d}".format(team, self.index)
    prop = RemoteProperty("DT_DOTA_PlayerResource")\
           .used_by(Property(dt_class, dt_prop))
    return prop.get_value(self)

  earned_gold = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_EndScoreAndSpectatorStats", "m_iTotalEarnedGold"))
  """
  The total earned gold by the user. This is not net worth; it should be used to
  calculate gpm and stuff.
  """

  name = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iszPlayerNames"))
  """
  The Steam name of the player, at the time of the game being played.
  """

  steam_id = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iPlayerSteamIDs"))
  """
  The Steam ID of the player.
  """

  team = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iPlayerTeams"))\
    .apply(MapTrans(TEAM_VALUES))
  """
  The player's team. Possible values are

  * ``"radiant"``
  * ``"dire"``
  * ``"spectator"``
  """

  last_hits = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iLastHitCount"))
  """
  The number of last hits on creeps that the player has.
  """

  denies = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iDenyCount"))
  """
  The number of denies on creeps that the player has.
  """

  kills = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iKills"))
  """
  The number of times the player has killed an enemy hero.
  """

  deaths = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iDeaths"))
  """
  The number of times the player has died.
  """

  assists = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iAssists"))
  """
  The number of assists the player has.
  """

  streak = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iStreak"))
  """
  The current kill-streak the player is on
  """

  buyback_cooldown_time = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource",
                             "m_flBuybackCooldownTime"))
  """
  The game time that the buyback will come off cooldown. If this is 0, the
  player has not bought back.
  """

  last_buyback_time = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iLastBuybackTime"))
  """
  The :attr:`~GameInfo.game_time` that the player bought back.
  """

  @property
  def has_buyback(self):
    """
    Can the player buyback (regardless of their being alive or dead).
    """
    current_time = self.stream_binding.info.game_time
    return current_time >= self.buyback_cooldown_time

  @property
  def total_gold(self):
    """
    The sum of the player's reliable and unreliable gold.
    """
    return self.reliable_gold + self.unreliable_gold
