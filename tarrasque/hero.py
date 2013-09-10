import re

from .binding import *
from .entity import *
from .properties import *
from .basenpc import *

@register_entity("DT_DOTA_BaseNPC_Hero")
@register_entity_wildcard("DT_DOTA_Unit_Hero_*")
class Hero(BaseNPC):
  """
  While all hero classes inherit from this class, it is unlikely that this class
  will ever need to be instantiated.
  """

  def __new__(cls, *args, **kwargs):
    ehandle = kwargs.get("ehandle")
    stream_binding = kwargs.get("stream_binding")

    world = stream_binding.world
    dt = world.recv_tables[world.classes[ehandle]].dt

    cls_name = dt.replace("DT_DOTA_Unit_Hero_", "").replace(" ", "")
    cls = type(str(cls_name), (Hero,), {})
    register_entity(dt)(cls)

    instance = object.__new__(cls, *args, **kwargs)
    cls.__init__(instance, *args, **kwargs)
    if not instance.name:
      split_name = [s for s in re.split("([A-Z][^A-Z]*)", cls_name) if s]
      instance.name = " ".join(split_name)
    return instance

  name = None
  """
  The name of the hero. For the base :class:`Hero` class, this is ``None``,
  but it is set when a subclass is created in the __new__ method.
  """

  xp = Property("DT_DOTA_BaseNPC_Hero", "m_iCurrentXP")
  """
  The hero's experience.
  """

  respawn_time = Property("DT_DOTA_BaseNPC_Hero", "m_flRespawnTime")
  """
  Appears to be the absolute time that the hero respawns. See
  :attr:`~GameInfo.game_time` for the current time of the tick to compare.

  TODO: Check this on IRC
  """

  ability_points = Property("DT_DOTA_BaseNPC_Hero", "m_iAbilityPoints")
  """
  Seems to be the number of ability points the player can assign.

  TODO: Check this on IRC
  """

  natural_strength = Property("DT_DOTA_BaseNPC_Hero", "m_flStrength")
  """
  The hero's strength from levels.
  """

  natural_agility = Property("DT_DOTA_BaseNPC_Hero", "m_flAgility")
  """
  The hero's agility from levels.
  """

  natural_intelligence = Property("DT_DOTA_BaseNPC_Hero", "m_flIntellect")
  """
  The hero's intelligence from levels.
  """

  strength = Property("DT_DOTA_BaseNPC_Hero", "m_flStrengthTotal")
  """
  The hero's strength (from levels, items, and the attribute bonus).
  """

  agility = Property("DT_DOTA_BaseNPC_Hero", "m_flAgilityTotal")
  """
  The hero's agility (from levels, items, and the attribute bonus).
  """

  intelligence = Property("DT_DOTA_BaseNPC_Hero", "m_flIntellectTotal")
  """
  The hero's intelligence (from levels, items, and the attribute bonus).
  """

  recent_damage = Property("DT_DOTA_BaseNPC_Hero", "m_iRecentDamage")
  """
  Recent damage taken? Would make sense for figuring out when to cancel
  tranquils and stuff.

  TODO: figure out exactly what this is
  """

  spawned_at = Property("DT_DOTA_BaseNPC_Hero", "m_flSpawnedAt")
  """
  The time (in :attr:`~GameInfo.game_time` units) the hero spawned at.

  TODO: Check this in game.
  """

  replicating_hero = Property(
    "DT_DOTA_BaseNPC_Hero", "m_hReplicatingOtherHeroModel"
  ).apply(EntityTrans())
  """
  The :class:`Hero` the current hero is "replicating" [#f1]_. If the instance
  is not an illusion (which use the :class:`Hero` class also), this will be
  ``None``. There is no guarantee that that this hero will exist (see
  :attr:`DotaEntity.exists`) if the hero is someone like Phantom Lancer, who
  may have an illusion which creates other illusions, and then dies.
  However, this is still a useful property for tracking illusion creation
  chains
  """

  _player_id = Property("DT_DOTA_BaseNPC_Hero", "m_iPlayerID")

  @property
  def player(self):
    """
    The player that is playing the hero.
    """
    for player in self.stream_binding.players:
      if player.index == self._player_id:
        return player
    return None
