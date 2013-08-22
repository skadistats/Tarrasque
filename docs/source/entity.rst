Dota Entity
-----------

.. module:: tarrasque.entity
   :synopsis: Contains the DotaEntity class and entity class registration
              decorators

.. class:: DotaEntity(ehandle, stream_binding)

       A base class for all Tarrasque entity classes.

       If you plan to manually initialise this class or any class inheriting from
       it (and I strongly recommend against it), pass initialisation arguments by
       name.

   .. attribute:: ehandle

          The ehandle of the entity. Used to identify the entity across ticks.

   .. attribute:: dt_key

          The dt name that corresponds to the DT class that the Tarrasque
          :class:`DotaEntity` subclass wraps.

          For :class:`DotaEntity` instances, this is ``"DT_BaseEntity"``

   .. attribute:: stream_binding

          The :class:`StreamBinding` object that the entity is bound to. The
          source of all information in a Tarrasque entity class.

   .. attribute:: world

          The world object for the current tick. Accessed via
          :py:attr:`stream_binding`.

   .. attribute:: tick

          The current tick number.

   .. attribute:: properties

          The value of `self.world.find(self.ehandle)` for the current tick.

   .. attribute:: exists

          True if the ehandle exists in the current tick's world. Examples of
          this not being true are when a :class:`Hero` entity that represents an
          illusion is killed, or at the start of a game when not all heroes have
          been chosen.

   .. classmethod:: get_all(stream_binding)

          This method uses the class's :attr:`dt_key` attribute to find all
          instances of the class in the stream binding's current tick, and then
          initialise them and return them as a list.

          While this method seems easy enough to use, prefer other methods where
          possible. For example, using this function to find all
          :class:`Player` instances will return 11 or more players, instead of
          the usual 10, where as :attr:`StreamBinding.players` returns the
          standard (and correct) 10.

.. decorator:: register_entity(dt_key)

       Register a class that Tarrasque will use to represent dota entities with
       the given DT key. This class decorator automatically sets the
       :attr:`~DotaEntity.dt_key` attribute.

.. decorator:: register_entity_wildcard(regexp)

       Similar to :obj:`register_entity`, will register a class, but instead of
       specifying a specific DT, use a regular expression to specify a range of
       DTs. For example, :class:`Hero` uses this to supply a model for all
       heroes, i.e.::

           from tarrasque.entity import *

           @register_entity_wildcard("DT_DOTA_Unit_Hero_(.*)")
           class Hero(DotaEntity):
               def __new__(cls, *args, **kwargs):
                   # Use __new__ to dynamically generate individual hero classes
                   # See tarrasque/hero.py for actual implementation
                   return cls(*args, **kwargs)

       A wildcard registration will not override a specific DT registration via
       :obj:`register_entity`.
