from .properties import *
from .lanecreep import LaneCreep
from .entity import register_entity
import re

"""
A class for neutral creeps, does not seem to include Roshan (needs confirmation)
"""
@register_entity('DT_DOTA_BaseNPC_Creep_Neutral')
class NeutralCreep(LaneCreep):
    name = Property("DT_BaseEntity", "m_nModelIndex")\
        .apply(StringTableTrans("modelprecache"))\
        .apply(FuncTrans(lambda n: n[0]))\
        .apply(FuncTrans(lambda n: re.findall('(?<=/)[a-z\_]+(?=\.mdl)', n)[0]))
        """
        Uses regexp to get a more readable creep name from the model name
        """
