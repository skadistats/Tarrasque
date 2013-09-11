import functools

from skadi.engine import game_event

from .properties import *

def requires_humanize(func):
  @functools.wraps(func)
  def inner(self, *args, **kwargs):
    if not self._humanize:
      event_list = self.stream_binding.prologue.game_event_list
      self._humanize = game_event.humanize(self._data, event_list)

    return func(self, *args, **kwargs)
  return inner

class GameEvent(object):
  """
  Base class for all game events. Handles humanise and related things.
  """

  def __init__(self, stream_binding, data):
    # Note that game events can't really be tracked across ticks, so
    # we just pass the data

    self._class_index, self._attrs = self._data = data

    self.stream_binding = stream_binding

    # The output of humanize(self._data, game_event_list)
    self._humanize = None

  @property
  @requires_humanize
  def properties(self):
    return self._humanize[1]

  @property
  @requires_humanize
  def name(self):
    """
    The name of the GameEvent. i.e. ``"dota_combatlog"``, ``"dota_chase_hero"``.
    """
    return self._humanize[0]
