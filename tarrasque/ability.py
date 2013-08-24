from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTABaseAbility")
@register_entity_wildcard("DT_DOTA_Ability_*")
@register_entity_wildcard("DT_DOTA_Unit_Ability_*")
@register_entity_wildcard("DT_Ability_*")
class BaseAbility(DotaEntity):
    level = Property("DT_DOTABaseAbility", "m_iLevel")

    off_cooldown_time = Property("DT_DOTABaseAbility", "m_fCooldown")

    @property
    def is_on_cooldown(self):
        current_time = self.stream_binding.rules.game_time
        return current_time <= self.off_cooldown_time

    cooldown_length = Property("DT_DOTABaseAbility", "m_flCooldownLength")

    mana_cost = Property("DT_DOTABaseAbility", "m_iManaCost")

    cast_range = Property("DT_DOTABaseAbility", "m_iCastRange")

    @property
    def is_passive(self):
        return self.mana_cost == 0

    @property
    def is_ultimate(self):
        hero = self.owner
        index = -1
        for i, ability in enumerate(hero.abilities):
            if ability == self:
                index = i
        return index == len(hero.abilities) - 2 # -1 for 0, -1 for stats

    @property
    def is_castable(self):
        return self.level > 0 and not self.is_on_cooldown and self.owner.mana > self.mana_cost
