Player
------

.. class:: Player(ehandle, stream_binding)

   Inherits from :class:`DotaEntity`.

   Represents a player in the game. This can be a player who is controlling a
   hero, or a "player" that is spectating.

   .. attribute:: dt_key

      For :class:`Player`, ``"DT_DOTAPlayer"``. However, much of the information
      in this class comes from ``"DT_DOTA_PlayerResource"``, so
      :attr:`~DotaEntity.properties` is not enough.

   .. attribute:: index

      The index of the player in the game. i.e. 0 is the first player on the
      radiant team, 9 is the last on the dire

      This is -1 for the undefined player, which should be ignored.

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

   .. attribute:: net_worth

      The net worth of the player.

      TODO: Check this is actually the net worth

   .. attribute:: name

      The Steam name of the player, at the time of the game being played.

   .. attribute:: steam_id

      The Steam ID of the player.

   .. attribute:: team

      The player's team. Possible values are

      * ``"radiant"``
      * ``"dire"``
      * ``"spectator"``

   .. attribute:: last_hits

      The number of last hits on creeps that the player has.

   .. attribute:: denies

      The number of denies on creeps that the player has.

   .. attribute:: kills

      The number of hero kills the player has.

   .. attribute:: deaths

      The number of times the player has died.

   .. attribute:: assists

      The number of assists the player has.

   .. attribute:: streak

      The current kill-streak the user is on

   .. attribute:: buyback_cooldown_time

      The :attr:``~GameRules.game_time`` that the player can buy back.

   .. attribute:: has_buyback

      Can the player buyback (regardless of their being alive or dead).
