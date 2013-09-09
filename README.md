Tarrasque
=========

[![Build Status](https://travis-ci.org/bluepeppers/Tarrasque.png?branch=master)](https://travis-ci.org/bluepeppers/Tarrasque)

A mapping from entities in Dota 2 replays to Python
objects. i.e. replays for humans.

Documentation
-------------

Documentation is hosted by ReadTheDocs.org, and can be found
[here](https://tarrasque.readthedocs.org/)

Example usage
-------------

For more examples, see the examples directory

### Hero and Player manipulation

Very basic example, but should show the power of Tarrasque

    from tarrasque import *

    replay = StreamBinding.from_file("./demo/PL.dem", start_tick="game")
    for player in replay.players:
        print "{} is playing {}".format(player.name, player.hero.name)

### Generating a gold graph

    from tarrasque import *

    # Create a StreamBinding object; this object allows us to create
    # "views" onto the replay data. Using the from_file, we pass it
    # the name of the replay file, and the "tick" we want to start
    # at. However, instead of giving a precise tick, we pass "game",
    # which tells the StreamBinding to start from the tick where the
    # game time hits 0
    replay = StreamBinding.from_file("./demo/PL.dem", start_tick="game")

    for player in replay.players:
        print "{} is playing {}".format(player.name, player.hero.name)

    # Example output for the replay ./demo/PL.dem
    #  Savlon is playing Phantom Lancer
    #  once is playing Necrolyte
    #  arrow6 is playing Nyx_ Assassin
    #  niv3k is playing Tusk
    #  Gyozmo is playing Slark
    #  xportugeex28 is playing Batrider
    #  andreissoares is playing Bounty Hunter
    #  williamkork is playing Bristleback
    #  Nenette1987 is playing Nevermore
    #  Ben_Laden is playing Ogre_ Magi

    # As the objects (such as player, player.hero) are just views over
    # the data, when you change the tick, the data they report will
    # change. So graphing things is just a case of remembering the
    # values

    # If you have matplotlib installed, this will graph a hero's
    # current gold

    hero = replay.players[0].hero
    print "Graphing for {}, played by {}".format(hero.name,
                                                 hero.player.name)

    gold_data = []
    tick_data = []

    # Start at "game" which is the time the game clock hits 0, stop at
    # "postgame", which is when the ancient is destroyed. Step of 30
    # so we only sample data once a second
    for tick in replay.iter_ticks(start="game", end="postgame", step=30):

        # Players have gold, not heroes. This deals with people
        # swapping heroes and stuff.
        gold_data.append(hero.player.total_gold)
        tick_data.append(tick)

    # Get our plotting library
    import matplotlib.pyplot as plt
    # And plot the gold against the ticks
    plt.plot(tick_data, gold_data)

    # And then show it
    plt.show()
    # Or save it
    plt.savefig("./output.png")
