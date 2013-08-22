Game Rules
==========

.. module:: tarrasque.gamerules

.. class:: GameRules

       Inherits from :class:`DotaEntity`

       The GameRules contains the macro state of the game; the stage of the game
       that the tick is in, whether the tick is in day or night, the length of
       the game, etc etc.

   .. attribute:: game_state

          The state of the game. Potential values are:

          * ``"loading"`` - Players are loading into the game
          * ``"draft"`` - The draft state has begun
          * ``"pregame"`` - The game has started but creeps have not been
            spawned
          * ``"game"`` - The main game, between the first creep spawn and the
            ancient being destroyed
          * ``"postgame"`` - The post game, display of the scores
