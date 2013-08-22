Player
------

.. class:: Player(ehandle, stream_binding)

   Inherits from :class:`DotaEntity`.

   .. attribute:: dt_key

      For :class:`Player`, ``"DT_DOTAPlayer"``. However, much of the information
      in this class comes from ``"DT_DOTA_PlayerResource"``, so
      :attr:`~DotaEntity.properties` is not enough.

   .. attribute:: index

      The index of the player in the game. i.e. 0 is the first player on the
      radiant team, 9 is the last on the dire

   .. attribute:: hero

      The :class:`Hero` that the player is playing in the tick. May be ``None``
      if the player has yet to choose a hero. May change when the
      :attr:`~GameRules.game_state` is ``"pre_game"``, due to players swapping
      their heroes.

   .. attribute:: unreliable_gold

      The player's unreliable gold in that tick

   .. attribute:: reliable_gold

      The player's reliable gold in the tick

   .. attribute:: total_gold

      The sum of the player's reliable and unreliable gold.

   .. attribute:: name

      The Steam name of the player, at the time of the game being played.

   .. attribute:: team

      The player's team. Possible values are

      * ``"radiant"``
      * ``"dire"``
      * ``"spectator"``
