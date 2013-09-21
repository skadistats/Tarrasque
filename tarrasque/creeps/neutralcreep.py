from ..properties import *
from .lanecreep import LaneCreep
from ..entity import register_entity
import re


@register_entity('DT_DOTA_BaseNPC_Creep_Neutral')
class NeutralCreep(LaneCreep):
    """
    A class for neutral creeps, does not seem to include Roshan (needs
    confirmation)
    """

    # The regexp cleans up the model cache to give a half readable name
    name = Property("DT_BaseEntity", "m_nModelIndex")\
        .apply(StringTableTrans("modelprecache"))\
        .apply(FuncTrans(lambda n: n[0]))\
        .apply(FuncTrans(lambda n: re.findall('(?<=/)[a-z\_]+(?=\.mdl)', n)[0]))
    """
    A name for the creep. While this name is understandable, it's not something
    you would want to print to a user.
    """
