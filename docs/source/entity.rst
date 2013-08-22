Tarrasque Dota Entities
=======================

The :class:`DotaEntity` class is the base class for all Tarrasque entity
classes. See individual classes documentation for details on their properties.

Dota Entities:

.. toctree::
   :maxdepth: 2

   gamerules

Dota Entity
===========

.. class:: DotaEntity(ehandle, stream_binding)

       A base class for all Tarrasque entity classes.

       If you plan to manually initialise this class or any class inheriting from
       it (and I strongly recommend against it), pass initialisation arguments by
       name.

   .. attribute:: ehandle

          The ehandle of the entity. Used to identify the entity across ticks.

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
