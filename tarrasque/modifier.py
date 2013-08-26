from .properties import *

class Modifier(object):
  """
  Represents a modifier on an entity. Modifiers are sustained affects on
  entities such as buffs and debufs. For example, the invulnerability aura
  provided by the fountain is exposed as a Modifier.
  """

  def __init__(self, mhandle, stream_binding):
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
    return self.stream_binding.modifiers.by_mhandle[self.mhandle][1]

  name = ModifierProperty("name")\
         .apply(StringTableTrans("ModifierNames"))\
         .apply(FuncTrans(lambda v: v[0]))
  """
  The name of the modifier.
  """

  caster = ModifierProperty("caster")\
           .apply(EntityTrans())
  """
  The caster of the modifier.
  """

  def __repr__(self):
    if self.name:
      return "Modifier('{}')".format(self.name)
    else:
      super(Modifier, self).__repr__()