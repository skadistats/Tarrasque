from .properties import *

class Modifier(object):
  """
  Represents a modifier on an entity. Modifiers are sustained affects on
  entities such as buffs and debufs. For example, the invulnerability aura
  provided by the fountain is exposed as a Modifier.
  """

  def __init__(self, parent, mhandle, stream_binding):
    self.parent = parent
    """
    The :class:`DotaEntity` that has this modifier.
    """

    self.mhandle = mhandle
    """
    The "mhandle" of the Modifier, used to track it across ticks.
    """

    self.stream_binding = stream_binding

  @property
  def world(self):
    return self.stream_binding.world

  @property
  def properties(self):
    modifiers = self.stream_binding.modifiers
    return modifiers.by_parent[self.parent.ehandle][self.mhandle]

  @property
  def exists(self):
    modifiers = self.stream_binding.modifiers
    return self.mhandle in modifier.by_parent.get(self.parent.ehandle, {})

  name = ModifierProperty("name")
  """
  The name of the modifier.
  """

  caster = ModifierProperty("caster")\
           .apply(EntityTrans())
  """
  The caster of the modifier.
  """

  aura = ModifierProperty("aura")
  """
  Boolean determining if the modifier is placed by an aura or not.
  """

  ability_level = ModifierProperty("ability_level")
  """
  The level of the ability that caused this modifier.
  """

  ability = ModifierProperty("ability")\
            .apply(EntityTrans())
  """
  The ability that caused this modifier.
  """

  created = ModifierProperty("creation_time")
  """
  The game time that the modifier was applied.
  """

  def __repr__(self):
    if self.name:
      return "Modifier('{}')".format(self.name)
    else:
      return super(Modifier, self).__repr__()