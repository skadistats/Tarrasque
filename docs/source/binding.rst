Stream Binding
==============

.. class:: StreamBinding(demo[, start_tick=5000])

   The :class:`StreamBinding` class is Tarrasque's metaphor for the replay.
   Every Tarrasque entity class has a reference to an instance of this
   class, and when the tick of the instance changes, the data returned by
   those classes changes. This makes it easy to handle complex object graphs
   without explicitly needing to pass the Skadi demo object around.

   .. staticmethod:: from_file(filename, *args, **kwargs)

          Loads the demo from the filename, and then initialises the
          :class:`StreamBinding` with it, along with any other passed arguments.

   .. attribute:: world

          The Skadi world object for the current tick.

   .. attribute:: tick

          The current tick

   .. method:: iter_ticks([start, [end, [step=1]]])

          A generator that iterates through the demo's ticks and updates the
          :class:`StreamBinding` to that tick. Yields the current tick.

          The start parameter defines the tick to iterate from, and if not set,
          the :attr:`StreamBinding.tick` attribute will be used.

          The end parameter defines the point to stop iterating; if not set,
          the iteration will continue until the end of the replay [#endNote]_.

          The step parameter is the number of ticks to consume before yielding
          the tick; the default of one means that every tick will be yielded. Do
          not assume that the step is precise; the gap between two ticks will
          always be larger than the step, but usually not equal to it.

   .. method:: go_to_tick(tick)

          Moves too the given tick, or the nearest tick after it.

   .. attribute:: players

          A list of :class:`Player` objects, one for each player in the game.
          This excludes spectators and other non-hero-controlling players.

   .. attribute:: rules

          The :class:`GameRules` object for the replay.

.. rubric:: Footnotes

.. [#endNote] The end of the replay includes the post game results screen, so if
              you want to iterate until the ancient dies, check
              :attr:`GameRules.game_state`.
