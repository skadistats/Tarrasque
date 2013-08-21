Tarrasque
=========

A mapping from entities in Dota 2 replays to Python
objects. i.e. replays for humans.

Example usage
-------------

    from tarrasque import *
    
    # Create a StreamBinding object; this object allows us to create
    # "views" onto the replay data. Using the from_file, we pass it
    # the name of the replay file, and the tick we want to start at.
    replay = StreamBinding.from_file("./demo/PL.dem", 5000)
    
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
    
    # iter_ticks can iterate the ticks from 0, starting at a specific
    # tick, or between two ticks. Here we give it just a starting tick,
    # so it will iterate until the game has finished.
    for tick in replay.iter_ticks(5000):
        # We don't want to plot every tick, as there will be a ton
        # where nothing happens. There are roughly 30 ticks per
        # second, so we run this loop one a second
        if tick % 30 > 2:
            continue
        
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
