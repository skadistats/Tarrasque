from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTABaseAbility")
@register_entity_wildcard("DT_DOTA_Ability_*")
@register_entity_wildcard("DT_DOTA_Unit_Ability_*")
@register_entity_wildcard("DT_Ability_*")
class BaseAbility(DotaEntity):
    """
    Base class for all abilities. Currently does not delegate to other classes,
    but can do so.
    """

    level = Property("DT_DOTABaseAbility", "m_iLevel")
    """
    The number of times the ability has been leveled up.
    """

    off_cooldown_time = Property("DT_DOTABaseAbility", "m_fCooldown")
    """
    The time the ability comes off cooldown. Note that this does not reset
    once that time has been passed.
    """

    @property
    def is_on_cooldown(self):
        """
        Uses :attr:`off_cooldown_time` and :attr:`GameInfo.game_time` to
        calculate if the ability is on cooldown or not.
        """
        current_time = self.stream_binding.info.game_time
        return current_time <= self.off_cooldown_time

    cooldown_length = Property("DT_DOTABaseAbility", "m_flCooldownLength")
    """
    How long the goes on cooldown for every time it is cast.
    """

    mana_cost = Property("DT_DOTABaseAbility", "m_iManaCost")
    """
    The mana cost of the spell
    """

    cast_range = Property("DT_DOTABaseAbility", "m_iCastRange")
    """
    The distance from the hero's position that this spell can be cast/targeted
    at.
    """

    @property
    def is_ultimate(self):
        """
        Use's the abilities position in :attr:`Hero.abilities` to figure out if
        this is the ultimate ability.

        TODO: Check this is reliable
        """
        hero = self.owner
        index = -1
        for i, ability in enumerate(hero.abilities):
            if ability == self:
                index = i
        return index == len(hero.abilities) - 2 # -1 for 0, -1 for stats
