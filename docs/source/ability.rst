Ability
-------

.. class:: Ability(ehandle, stream_binding)

   Inherits from :class:``DotaEntity``.

   Base class for all abilities. Currently does not delegate to other classes,
   but can do so.

   .. attribute:: level

      The number of times the ability has been leveled up.

   .. attribute:: off_cooldown_time

      The time the ability comes off cooldown. Note that this does not reset
      once that time has been passed.

   .. attribute:: is_on_cooldown

      Uses :attr:``off_cooldown_time`` and :attr:``GameRules.game_time`` to
      calculate if the ability is on cooldown or not.

   .. attribute:: cooldown_length

      How long the goes on cooldown for every time it is cast.

   .. attribute:: mana_cost

      The mana cost of the spell

   .. attribute:: cast_range

      The distance from the hero's position that this spell can be cast/targeted
      at.

   .. attribute:: is_passive

      Assumes that passives are the only spells with zero mana cost.

      TODO: Check this on IRC

   .. attribute:: is_ultimate

      Use's the abilities position in :attr:``Hero.abilities`` to figure out if
      this is the ultimate ability.

      TODO: Check this is reliable

   .. attribute:: is_castable

      Can the ability be casted on an enemy in this tick.
