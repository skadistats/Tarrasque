API
===

Stream Binding
--------------

.. automodule:: tarrasque.binding
   :members: StreamBinding

Dota Entity
-----------

.. automodule:: tarrasque.entity
   :members:

Player
------

.. automodule:: tarrasque.player
   :members:

Game Info
---------

.. automodule:: tarrasque.gameinfo
   :members:

Ability
-------

.. automodule:: tarrasque.ability
   :members:

Base NPC
--------

.. automodule:: tarrasque.basenpc
   :members:

Hero
----

While each hero has a distinct class, not all have classes that are defined in
source code. This is because the :class:`Hero` class registers itself as a
wildcard on the DT regexp ``"DT_DOTA_Unit_Hero_*"``, and then dynamically
generates hero classes from the ehandle. The generated classes simply inherit
from the :class:`Hero` and have different values for :attr:`~Hero.dt_key` and
:attr:`~Hero.name`.

.. automodule:: tarrasque.hero
   :members:

Game Events
-----------

.. automodule:: tarrasque.gameevents
   :members:
