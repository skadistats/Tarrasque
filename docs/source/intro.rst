An Introduction to Tarrasque
============================

Tarrasque is a library, build around Skadi_, to allow the easy and
straightforward analysis of Dota 2 replays. While Skadi provides only
the raw data, Tarrasque allows you to deal in objects and relationships.
A comparison will show this best.

.. _Skadi: https://github.com/onethirtyfive/skadi

This code uses Skadi to print out the names of the players in the replay, along
with the name of the hero they are playing

::

   import io
   from skadi.engine import world as w
   from skadi.replay import demo as rd

   with io.open("demo.dem", 'r+b') as infile:
       demo = rd.construct(infile)
       for tick, string_tables, world in demo.stream(tick=5000):
           ehandle, player_resource = world.find_by_dt(player_resource_dt)

           for i in range(31):
               player_name_key = ("DT_DOTA_PlayerResource", "m_iszPlayerNames.%40s" % i)
               player_name = player_resource[player_name_key]
               if not player_name:
                   break
               hero_ehandle_key = ("DT_DOTA_PlayerResource", "m_hSelectedHero")
               hero_ehandle = player_resource[hero_ehandle_key]
               hero_dt = world.recv_tables[world.classes[hero_ehandle]].dt
               hero_name = hero_dt.replace("DT_DOTA_Unit_Hero_", "").replace("_", " ")
               print hero_name
           break

Using Tarrasque, this could be written as

::

   import tarrasque

   replay = tarrasque.StreamBinding.from_file("demo.dem", 5000)
   for player in replay.players:
       print player.name
       print player.hero.name

The code speaks for itself. Tarrasque makes it simple, easy and even fun to
analyse Dota 2 replays.

Tarrasque concepts for people who know what an ehandle is
---------------------------------------------------------

Tarrasque is a mapper between Dota2 entities (DT classes) and Python classes.
Every Tarrasque class that represents an entity has a
:attr:`~DotaEntity.dt_key` property that specifies the DT class that it
represents, and once instantiated, every Tarrasque class has a
:attr:`~DotaEntity.ehandle` property that is used to get information from
the world. The current world can be accessed via :attr:`~DotaEntity.world`,
and the results of ``world.find(self.ehandle)`` via
:attr:`~DotaEntity.properties`. All this and more is documented on
:class:`DotaEntity`.

Tarrasque concepts for people who don't know what an ehandle is
---------------------------------------------------------------

Think of Tarrasque as an ORM for Dota2, except the models are already
maintained, and you don't have to worry about the database. You don't have
to mess about writing code to deal with the (disgusting) stuff that Dota2 does
in its replays, as Tarrasque exposes the data to you in a manner that follows
Python conventions; you'll get a ``None`` object instead of -1, and the string
``"radiant"`` instead of the integer 2 (where appropriate. Tarrasque understands
that values have special meanings only in specific contexts). This allows you to
just use the data, and not need to worry about the stuff underneath.

The one major difference between a database ORM and Tarrasque is that while
most ORM models are statefull (that is, when the database changes, the model
stays the same until reloaded), Tarrasque models contain no state, other than
that which is needed to uniquely identify the instance (and now you know what an
ehandle is). This means that you never have to do ``hero.update(tick_number)``
or similar; all that is handled automatically via the :class:`StreamBinding`/
:class:`DotaEntity` abstraction.
