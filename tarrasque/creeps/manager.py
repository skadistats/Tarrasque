class CreepManager(object):
  """
  A general object that allows the user to access the creeps in the game.
  """

  def __init__(self, stream_binding):
    self.stream_binding = stream_binding

  @property
  def lane(self):
    """
    Returns all the living lane creeps on the map.
    """
    from .lanecreep import LaneCreep

    return [lc for lc in LaneCreep.get_all(self.stream_binding)
            if lc.is_alive]

  @property
  def neutrals(self):
    """
    Returns all the living neutral creeps on the map.
    """
    from .neutralcreep import NeutralCreep

    return [nc for nc in NeutralCreep.get_all(self.stream_binding)
            if nc.is_alive]