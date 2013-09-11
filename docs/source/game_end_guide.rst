Analysing game end states
=========================

One of the most common ways to get information about a game is to look
at the state of the game when the ancient has died. Finding that time
can be a fairly annoying process, but Tarrasque makes it quite
easy. This example moves to the final tick of the game and then prints
out statistics for the players::

    import tarrasque

    replay = tarrasque.StreamBinding.from_file("demo.dem", start_tick="postgame")

    for player in replay.players:
        print "{} - Gold: {} - KDA: {}/{}/{}".format(player.name,
               player.earned_gold, player.kills, player.deaths. player.assists)

The instruction to move to the end of the replay is in the
``start_tick`` argument to ``StreamBinding.from_file``. By saying we
want to start at the ``"postgame"`` tick, we instruct Tarrasque to 1)
locate the tick where the ancient was destroyed, and 2) move to it.

One thing to note is that while you may want to use the
:attr:`GameInfo.game_time` attribute to calculate the GPM of a hero,
you should first subtract 90 (1 * 60 + 30) from that value, as while
the Dota2 ingame clock counts from the time the creeps spawn, the
replay attribute starts 1 minute 30 seconds earlier. To calculate GPM,
you might use something like this::

    import tarrasque

    replay = tarrasque.StreamBinding.from_file("demo.dem",
                         start_tick="postgame")

    for player in replay.players:
        gpm = player.earned_gold * 60 / (replay.info.game_time - 90)
        print "{} - GPM: {}".format(player.name, gpm)

Note also that we multiply by 60, as :attr:`GameInfo.game_time` is in
seconds, not minutes.
