from ..hero import Hero
from ..properties import *
from ..entity import *
from ..ability import BaseAbility

@register_entity('DT_DOTA_Unit_Hero_LoneDruid')
class LoneDruid(Hero):
    """
    A specialized class for the hero Lone Druid
    """

    @property
    def bear(self):
        return self.abilities[0].bear
@register_entity('DT_DOTA_Ability_LoneDruid_SpiritBear')
class SummonBear(BaseAbility):
    """
    A specialized class for Lone Druid's summon bear ability
    """

    bear = Property('DT_DOTA_Ability_LoneDruid_SpiritBear', 'm_hBear')\
           .apply(EntityTrans())

@register_entity('DT_DOTA_Unit_SpiritBear')
class SpiritBear(Hero):
    """
    A class for LD's spirit bear
    """
