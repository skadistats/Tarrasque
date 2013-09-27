class BuildingManager(object):
  """
  A general object that allows the user to access the creeps in the game.
  """

  def __init__(self, stream_binding):
    self.stream_binding = stream_binding

  @property
  def towers(self):
    """
    A list of :class:`Tower` objects, one for each tower in the replay.
    This excludes dead towers.
    """
    from .tower import Tower
    return Tower.get_all(self.stream_binding)
	
  @property
  def barracks(self):
    """
    A list of :class:`Barrack` objects, one for each barrack in the replay.
    """
    from .barrack import Barrack
    return Barrack.get_all(self.stream_binding)
	
  @property
  def ancients(self):
    """
    A list of :class:`Ancient` objects, one for each ancient in the replay.
    """
    from .ancient import Ancient
    return Ancient.get_all(self.stream_binding)
