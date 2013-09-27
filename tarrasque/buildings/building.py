from ..basenpc import *

@register_entity("DT_DOTA_BaseNPC_Building")
class Building(BaseNPC):
  """
  Inherits from :class:`BaseNPC`.

  Represents a building in the game.
  """

@register_entity("DT_DOTA_BaseNPC_Tower")
class Tower(Building):
  """
  Inherits from :class:`Building`.

  Represents a Tower in the game.
  """

@register_entity("DT_DOTA_BaseNPC_Barracks")
class Barrack(Building):
  """
  Inherits from :class:`Building`.

  Represents a Barrack in the game.
  """

@register_entity("DT_DOTA_BaseNPC_Fort")
class Ancient(Building):
  """
  Inherits from :class:`Building`.

  Represents an Ancient in the game.
  """
