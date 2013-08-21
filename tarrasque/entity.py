import inspect
from importlib import import_module
import sys
import re

from .consts import *

global ENTITY_CLASSES
ENTITY_CLASSES = {}
global ENTITY_WILDCARDS
ENTITY_WILDCARDS = []

def register_entity(dt_name):
  def inner(cls):
    ENTITY_CLASSES[dt_name] = cls
    cls.dt_key = dt_name
    return cls
  return inner

def register_entity_wildcard(regexp):
  def inner(cls):
    ENTITY_WILDCARDS.append((re.compile(regexp), cls))
    return cls
  return inner

def create_default_class(dt_name, world):
  return DotaEntity

@register_entity("DT_BaseEntity")
class DotaEntity(object):
  def __init__(self, stream_binding, ehandle):
    self.stream_binding = stream_binding
    self.ehandle = ehandle

  @property
  def world(self):
    return self.stream_binding.world

  @property
  def tick(self):
    return self.stream_binding.tick

  @property
  def properties(self):
    """
    Return the data associated with the handle for the current tick.
    """
    return self.world.find(self.ehandle)

  @property
  def exists(self):
    try:
      self.world.find(self.ehandle)
    except KeyError:
      return False
    else:
      return True

  @classmethod
  def get_all(cls, binding):
    output = []
    for ehandle, _ in binding.world.find_all_by_dt(cls.dt_key).items():
      output.append(cls(ehandle=ehandle, stream_binding=binding))
    return output