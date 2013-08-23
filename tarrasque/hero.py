import re

from .binding import *
from .entity import *
from .properties import *
from .basenpc import *

@register_entity("DT_DOTA_BaseNPC_Hero")
@register_entity_wildcard("DT_DOTA_Unit_Hero_*")
class Hero(BaseNPC):
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

  xp = Property("DT_DOTA_BaseNPC_Hero", "m_iCurrentXP")

  respawn_time = Property("DT_DOTA_BaseNPC_Hero", "m_flRespawnTime")

  ability_points = Property("DT_DOTA_BaseNPC_Hero", "m_iAbilityPoints")

  strength = Property("DT_DOTA_BaseNPC_Hero", "m_flStrength")

  agility = Property("DT_DOTA_BaseNPC_Hero", "m_flAgility")

  intellect = Property("DT_DOTA_BaseNPC_Hero", "m_flIntellect")

  strength_total = Property("DT_DOTA_BaseNPC_Hero", "m_flStrengthTotal")

  agility_total = Property("DT_DOTA_BaseNPC_Hero", "m_flAgilityTotal")

  intellect_total = Property("DT_DOTA_BaseNPC_Hero", "m_flIntellectTotal")

  recent_damage = Property("DT_DOTA_BaseNPC_Hero", "m_iRecentDamage")

  player_id = Property("DT_DOTA_BaseNPC_Hero", "m_iPlayerID")

  spawned_at = Property("DT_DOTA_BaseNPC_Hero", "m_flSpawnedAt")

  replicating_hero = Property(
    "DT_DOTA_BaseNPC_Hero", "m_hReplicatingOtherHeroModel"
  ).apply(EntityTrans())
