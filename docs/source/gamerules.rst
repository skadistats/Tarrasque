Game Rules
==========

.. class:: GameRules

   Inherits from :class:`DotaEntity`

   The GameRules contains the macro state of the game; the stage of the game
   that the tick is in, whether the tick is in day or night, the length of
   the game, etc etc.

   .. rubric:: Time Attributes

   These attributes detail various times of note in the match.

   .. attribute:: game_time

      The time in seconds of the current tick.

   .. attribute:: load_time
   .. attribute:: draft_start_time
   .. attribute:: pregame_start_time
   .. attribute:: game_start_time
   .. attribute:: game_end_time

      The time when the various changes to :attr:`game_state` happened. These
      values will be ``None`` until the event has passed, meaning that they are
      not useful for looking ahead to find out when certain events happened,
      though one could skip to the end of the replay to find their values.

      TODO: check or verify on IRC about draft_start_time, Skadi wiki is
      ambiguous

   .. rubric:: Match Information Attributes

   These attributes contain the defining characteristics of the match that are
   (for the most part), not tick specific.

   .. attribute:: match_id

      The unique match id, used by the Steam API and stuff (i.e. DotaBuff and
      friends).

   .. attribute:: game_mode

      The mode of the dota game. Possible values are:

      * ``"all-pick"``
      * ``"captain's mode"``
      * ``"random draft"``
      * ``"single draft"``
      * ``"all random"``
      * ``"reverse captain's mode"``

   .. attribute:: game_state

      The state of the game. Potential values are:

      * ``"loading"`` - Players are loading into the game
      * ``"draft"`` - The draft state has begun
      * ``"pregame"`` - The game has started but creeps have not been
        spawned
      * ``"game"`` - The main game, between the first creep spawn and the
        ancient being destroyed
      * ``"postgame"`` - The post game, display of the scores

   .. attribute:: pick_state

      The current pick/ban that is happening. ``None`` if no pick or ban is
      happening. If the :attr:`game_mode` is not ``"captain's mode"``, the
      possible values are:

      * ``"all-pick"``
      * ``"single draft"``
      * ``"random draft"``
      * ``"all random"``

      Otherwise, the current pick and ban is returned in a tuple of the type of
      draft action and the index. For example, if the current tick was during
      the 5th ban of a captains mode game, the value of :attr:`pick_state` would
      be ``("ban", 5)``. :attr:`active_team` could then be used to work out who
      is banning. Alternatively, if it was the 2nd pick of the game, it would be
      ``("pick", 2)``.

   .. rubric:: Team State attributes

   These attributes will be either ``"radiant"`` or ``"dire"`` except in
   situations where they have no meaning, in which case they should be ``None``.

   .. attribute:: starting_team

      The team that begins the draft.

   .. attribute:: pausing_team

      The team that is pausing the game, if it is being paused.

   .. attribute:: active_team

      The team that is currently banning/picking.

   .. attribute:: game_winner

      The winner of the game
