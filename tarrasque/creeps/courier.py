from ..properties import *
from ..basenpc import BaseNPC
from ..entity import register_entity

@register_entity("DT_DOTA_Unit_Courier")
class Courier(BaseNPC):
    """
    A courier
    """

    respawn_time = Property('DT_DOTA_Unit_Courier', 'm_flRespawnTime')
    """
    Returns a float of the courier's time until respawn.
    Returns 0.0 if courier is alive
    """


    is_flying = Property('DT_DOTA_Unit_Courier', 'm_bFlyingCourier')
    """
    Returns 0 if the courier is walking, 1 if it's flying
    """


    unusual_effect = Property('DT_DOTA_Unit_Courier', 'm_iUnusualParticleSystem')
    """
    Something about unusual couriers. -1 if not unusual.
    96 seems to be the ethereal flames effect, although it's possible that
    96 just refers to a general unusual particle thing. Not sure at all
    """
