import re

from .binding import *
from .entity import *

HERO_CLASSES = {}

def register_hero_class(dt):
  def inner(cls):
    HERO_CLASSES[dt] = cls
    return cls
  return inner

class Hero(DotaEntity):
  def __new__(cls, *args, **kwargs):
    ehandle = kwargs.get("ehandle")
    stream_binding = kwargs.get("stream_binding")

    world = stream_binding.world
    dt = world.recv_tables[world.classes[ehandle]].dt

    if dt in HERO_CLASSES:
      cls = HERO_CLASSES[dt]
      cls_name = cls.name or cls.__name__
    else:
      cls_name = dt.replace("DT_DOTA_Unit_Hero_", "").replace(" ", "")
      cls = type(cls_name, (Hero,), {})

    instance = DotaEntity.__new__(cls, *args, **kwargs)
    if not instance.name:
      split_name = [s for s in re.split("([A-Z][^A-Z]*)", cls_name) if s]
      instance.name = " ".join(split_name)
    return instance

  def __init__(self, player, *args, **kwargs):
    self.player = player
    DotaEntity.__init__(self, *args, **kwargs)

  name = None

  current_xp = Property("DT_DOTA_BaseNPC_Hero", "m_iCurrentXP")

@register_hero_class("DT_DOTA_Unit_Hero_PhantomLancer")
class PhantomLancer(Hero):
  pass