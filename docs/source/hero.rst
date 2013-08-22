Hero
----

While each hero has a distinct class, not all have classes that are defined in
source code. This is because the :class:`Hero` class registers itself as a
wildcard on the DT regexp ``"DT_DOTA_Unit_Hero_*"``, and then dynamically
generates hero classes from the ehandle. The generated classes simply inherit
from the :class:`Hero` and have different values for :attr:`~Hero.dt_key` and
:attr:`~Hero.name`.

.. class:: Hero

   Inherits from :class:`BaseNPC`.

   .. attribute:: name

      The name of the hero. For the base :class:`Hero` class, this is ``None``,
      but it is set when a subclass is created in the __new__ method.

   .. attribute:: dt_key

      For :class:`Hero`, ``"DT_DOTA_BaseNPC_Hero"``.

   .. attribute:: xp

      The hero's experience

   .. attribute:: respawn_time

      TODO: figure out exactly what this is

   .. attribute:: ability_points

      Most likely the number of ability points the player can assign.
      Potentially how many they have assigned + unassigned, in which case it
      would be equal to their level.

      TODO: figure out exactly what this is

   .. attribute:: strength
   .. attribute:: agility
   .. attribute:: intellect

      The hero's natural strength, agility and intellect, I think.

      TODO: figure out exactly what this is

   .. attribute:: strength_total
   .. attribute:: agility_total
   .. attribute:: intellect_total

      The hero's total (natural + items) strength, agility and intellect, I
      think. If this is confirmed to be so, will prob remove the ``_total``
      suffix and give the current strength, agility, intellect a ``natural_``
      prefix.

      TODO: figure out exactly what this is

   .. attribute:: recent_damage

      Recent damage taken? Would make sense for figuring out when to cancel
      tranquils and stuff.

      TODO: figure out exactly what this is

   .. attribute:: player_id

      Probably correlates to :attr:`Player.index`

      TODO: figure out exactly what this is

   .. attribute:: spawned_at

      The time(?) the hero spawned at? Prob, considering it can't be position.

      TODO: figure out exactly what this is

   .. attribute:: replicating_hero

      The :class:`Hero` the current hero is "replicating" [#f1]_. If the instance
      is not an illusion (which use the :class:`Hero` class also), this will be
      ``None``. There is no guarantee that that this hero will exist (see
      :attr:`DotaEntity.exists`) if the hero is someone like Phantom Lancer, who
      may have an illusion which creates other illusions, and then dies.
      However, this is still a useful property for tracking illusion creation
      chains

.. rubric:: Footnotes

.. [#f1] The term replicating is a misnomer, as the replicating_hero property
         points to the :class:`Hero` that created the illusion, not the original
         hero.
