BaseNPC
-------

.. class:: BaseNPC

   Inherits from :class:`DotaEntity`.

   .. attribute:: dt_key

      For :class:`BaseNPC`, ``"DT_DOTA_BaseNPC"``

   .. attribute:: position

      The (x, y) position of the NPC in terms of the Dota2 map coordinates

   .. attribute:: life_state

      The state of the NPC's life (unsurprisingly). Possible values are:

      * ``"alive"`` - The hero is alive
      * ``"dying"`` - The hero is in their death animation
      * ``"dead"`` - The hero is dead
      * ``"respawnable"`` - The hero can be respawned
      * ``"discardbody"`` - The hero's body can be discarded

      ``"respawnable"`` and ``"discardbody"`` shouldn't occur in a Dota2 replay

   .. attribute:: level

      The NPC's level. See :attr:``Hero.ability_points`` for unspent level up
      ability points.

   .. attribute:: is_alive

      A simple boolean to test that the :attr:`life_state` is ``"alive"``
