from .entity import *

@register_entity("DT_DOTATeam")
class Teaminfo(object):

  def __init__(self, stream_binding, ehandle):
    self._stream_binding = stream_binding
    self._ehandle = ehandle

  team_number = Property("DT_Team", "m_iTeamNum")
  
  team_name = Property("DT_Team", "m_szTeamname")
  
  team = Property("DT_Team", "m_iTeamNum")\
    .apply(MapTrans(TEAMINFO_TEAM_VALUES))
  
  hero_kills = Property("DT_DOTATeam", "m_iHeroKills")

  tower_kills = Property("DT_DOTATeam", "m_iTowerKills")

  barrack_kills = Property("DT_DOTATeam", "m_iBarracksKills")

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

  def __hash__(self):
    return hash(self.ehandle)
