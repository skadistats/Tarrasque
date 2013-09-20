import inspect
from importlib import import_module
import sys
import re

from .consts import *
from .properties import *

global ENTITY_CLASSES
ENTITY_CLASSES = {}
global ENTITY_WILDCARDS
ENTITY_WILDCARDS = []

def register_entity(dt_name):
  """
  Register a class that Tarrasque will use to represent dota entities with
  the given DT key. This class decorator automatically sets the
  :attr:``~DotaEntity.dt_key`` attribute.
  """
  def inner(cls):
    ENTITY_CLASSES[dt_name] = cls
    cls.dt_key = dt_name
    return cls
  return inner

def register_entity_wildcard(regexp):
  """
  Similar to :obj:`register_entity`, will register a class, but instead of
  specifying a specific DT, use a regular expression to specify a range of
  DTs. For example, :class:`Hero` uses this to supply a model for all
  heroes, i.e.::

      from tarrasque.entity import *

      @register_entity_wildcard("DT_DOTA_Unit_Hero_(.*)")
      class Hero(DotaEntity):
          def __new__(cls, *args, **kwargs):
               # Use __new__ to dynamically generate individual hero classes
               # See tarrasque/hero.py for actual implementation
               return cls(*args, **kwargs)

  A wildcard registration will not override a specific DT registration via
  :obj:`register_entity`.
  """
  def inner(cls):
    ENTITY_WILDCARDS.append((re.compile(regexp), cls))
    return cls
  return inner

def find_entity_class(dt_name):
  """
  Returns the class that should be used to represent the ehandle with the given
  dt name.
  """
  if dt_name in ENTITY_CLASSES:
    return ENTITY_CLASSES[dt_name]
  for regexp, cls in ENTITY_WILDCARDS:
    if regexp.match(dt_name):
      return cls
  return DotaEntity

def create_entity(ehandle, stream_binding):
  """
  Finds the correct class for the ehandle and initialises it.
  """
  dt = stream_binding.world.fetch_recv_table(ehandle).dt
  cls = find_entity_class(dt)
  return cls(ehandle=ehandle, stream_binding=stream_binding)

@register_entity("DT_BaseEntity")
class DotaEntity(object):
  """
  A base class for all Tarrasque entity classes.

  If you plan to manually initialise this class or any class inheriting from
  it (and I strongly recommend against it), pass initialisation arguments by
  name.
  """

  def __init__(self, stream_binding, ehandle):
    self._stream_binding = stream_binding
    self._ehandle = ehandle

  team = Property("DT_BaseEntity", "m_iTeamNum")\
    .apply(MapTrans(TEAM_VALUES))
  """
  The team that the entity is on. Options are

  * ``"radiant"``
  * ``"dire"``
  """

  name = Property("DT_BaseEntity", "m_iName")\
    .apply(FuncTrans(lambda n: n if n else None))
  """
  The name of an entity. This will either be equal to the
  :attr:`DotaEntity.raw_name` or be overridden to be a name an end user might
  be more familiar with. For example, if :attr:`~DotaEntity.raw_name` is
  ``"dt_dota_nevermore"``, this value might be set to ``"Nevermore"`` or
  ``"Shadow Field"``.
  """

  raw_name = name
  """
  The raw name of the entity. Not very useful on its own.
  """

  owner = Property("DT_BaseEntity", "m_hOwnerEntity")\
    .apply(EntityTrans())
  """
  The "owner" of the entity. For example, a :class:``BaseAbility`` the hero
  that has that ability as its owner.
  """

  @property
  def ehandle(self):
    """
    The ehandle of the entity. Used to identify the entity across ticks.
    """
    return self._ehandle

  @property
  def stream_binding(self):
    """
    The :class:`StreamBinding` object that the entity is bound to. The
    source of all information in a Tarrasque entity class.
    """
    return self._stream_binding

  @property
  def world(self):
    """
    The world object for the current tick. Accessed via
    :attr:``stream_binding``.
    """
    return self.stream_binding.world

  @property
  def tick(self):
    """
    The current tick number.
    """
    return self.stream_binding.tick

  @property
  def properties(self):
    """
    Return the data associated with the handle for the current tick.
    """
    return self.world.find(self.ehandle)

  @property
  def exists(self):
    """
    True if the ehandle exists in the current tick's world. Examples of
    this not being true are when a :class:`Hero` entity that represents an
    illusion is killed, or at the start of a game when not all heroes have
    been chosen.
    """
    try:
      self.world.find(self.ehandle)
    except KeyError:
      return False
    else:
      return True

  @property
  def modifiers(self):
    """
    A list of the entitiy's modifiers. While this does not make sense on some
    entities, as modifiers can be associated with any entity, this is
    implemented here.
    """
    from .modifier import Modifier
    mhandles = self.stream_binding.modifiers.by_parent.get(self.ehandle, [])

    modifiers = []
    for mhandle in mhandles:
      modifier = Modifier(parent=self, mhandle=mhandle,
                          stream_binding=self.stream_binding)
      modifiers.append(modifier)
    return modifiers

  @classmethod
  def get_all(cls, binding):
    """
    This method uses the class's :attr:`dt_key` attribute to find all
    instances of the class in the stream binding's current tick, and then
    initialise them and return them as a list.

    While this method seems easy enough to use, prefer other methods where
    possible. For example, using this function to find all
    :class:`Player` instances will return 11 or more players, instead of
    the usual 10, where as :attr:`StreamBinding.players` returns the
    standard (and correct) 10.
    """
    output = []
    for ehandle, _ in binding.world.find_all_by_dt(cls.dt_key).items():
      output.append(cls(ehandle=ehandle, stream_binding=binding))
    return output

  def __eq__(self, other):
    if hasattr(other, "ehandle"):
      return other.ehandle == self.ehandle

    return False
