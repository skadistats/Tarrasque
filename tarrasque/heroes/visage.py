from ..hero import Hero
from ..properties import *
from ..entity import *
from ..basenpc import BaseNPC

@register_entity('DT_DOTA_Unit_Hero_Visage')
class Visage(Hero):
    """
    A specialized class for the hero Visage
    """
    
    @property
    def familiars(self):
        """
        Gets all familiars on the map.
        Seems to only work on living familiars
        """
        return Familiar.get_all(self.stream_binding)
    
@register_entity('DT_DOTA_Unit_VisageFamiliar')
class Familiar(BaseNPC):
    """
    A class for visage familiars
    """
