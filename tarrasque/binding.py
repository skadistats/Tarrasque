import collections

Snapshot = collections.namedtuple("Snapshot",
                                  "tick, user_messages, game_events, world,"
                                  " modifiers")

class StreamBinding(object):
  """
  The StreamBinding class is Tarrasque's metaphor for the replay. Every
  Tarrasque entity class has a reference to an instance of this
  class, and when the tick of the instance changes, the data returned by
  those classes changes. This makes it easy to handle complex object graphs
  without explicitly needing to pass the Skadi demo object around.
  """

  @property
  def user_messages(self):
    """
    The user messages for the current tick.
    """
    return self._snapshot.user_messages

  @property
  def game_events(self):
    """
    The game events in the current tick.
    """
    return self._snapshot.game_events

  # Just another layer of indirection
  # These are properties for autodoc reasons mostly
  @property
  def world(self):
    """
    The Skadi wold object for the current tick.
    """
    return self._snapshot.world

  @property
  def tick(self):
    """
    The current tick.
    """
    return self._snapshot.tick

  @property
  def demo(self):
    """
    The Skadi demo object that the binding is reading from.
    """
    return self._demo

  @property
  def modifiers(self):
    """
    The Skadi modifiers object for the tick.
    """
    return self._snapshot.modifiers

  @property
  def string_tables(self):
    """
    The string_table provided by Skadi.
    """
    return self._stream.string_tables

  def __init__(self, demo, start_tick=5000):
    self._demo = demo
    self.go_to_tick(start_tick)

  def iter_ticks(self, start=None, end=None, step=1):
    """
    A generator that iterates through the demo's ticks and updates the
    :class:`StreamBinding` to that tick. Yields the current tick.

    The start parameter defines the tick to iterate from, and if not set,
    the :attr:`StreamBinding.tick` attribute will be used.

    The end parameter defines the point to stop iterating; if not set,
    the iteration will continue until the end of the replay.

    .. note:: The end of the replay includes the post game results screen, so if
              you want to iterate until the ancient dies, check
              :attr:`GameRules.game_state`.

    The step parameter is the number of ticks to consume before yielding
    the tick; the default of one means that every tick will be yielded. Do
    not assume that the step is precise; the gap between two ticks will
    always be larger than the step, but usually not equal to it.
    """

    if start is None:
      start = self.tick
    if end is not None:
      assert start < end

    last_tick = start - step - 1
    self._stream = self.demo.stream(tick=start)
    for snapshot in self._stream:
      self._snapshot = Snapshot(*snapshot)

      if end is not None and self.tick >= end:
        break

      if self.tick - last_tick < step:
        continue
      else:
        last_tick = tick

      yield self.tick

  def go_to_tick(self, tick):
    """
    Moves too the given tick, or the nearest tick after it.
    """
    self._stream = self.demo.stream(tick=tick)
    self._snapshot = Snapshot(*next(iter(self._stream)))

  def __iter__(self):
    return self.iter_ticks()

  @property
  def players(self):
    """
    A list of :class:`Player` objects, one for each player in the game.
    This excludes spectators and other non-hero-controlling players.
    """
    from . import Player

    return [p for p in Player.get_all(self) if
            p.index != None and p.team != "spectator"]

  @property
  def rules(self):
    """
    The :class:`GameRules` object for the replay.
    """
    from .gamerules import GameRules
    rules = GameRules.get_all(self)
    assert len(rules) == 1
    return rules[0]


  @staticmethod
  def from_file(filename, *args, **kwargs):
    """
    Loads the demo from the filename, and then initialises the
    :class:`StreamBinding` with it, along with any other passed arguments.
    """
    import skadi, skadi.demo
    import io

    f = io.open(filename, "r+b")
    prologue = skadi.load(f)
    demo = skadi.demo.construct(prologue, f)

    return StreamBinding(demo, *args, **kwargs)