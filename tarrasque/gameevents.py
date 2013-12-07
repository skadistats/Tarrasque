import functools
import re

from skadi.engine import game_event

from .properties import *

global EVENT_CLASSES
EVENT_CLASSES = {}
global EVENT_WILDCARDS
EVENT_WILDCARDS = []

def register_event(event_name):
    """
    Register a class as the handler for a given event.
    """
    def inner(event_class):
        EVENT_CLASSES[event_name] = event_class
        return event_class
    return inner

def register_event_wildcard(event_pattern):
    """
    Same as :func:`register_event` but uses a regex pattern to match, instead of
    a static game event name.
    """
    def inner(event_class):
        EVENT_WILDCARD.append((re.compile(event_wildcard), event_class))
        return event_class
    return inner

def find_game_event_class(event_name):
    """
    Given the name of an event, finds the class that should be used to represent
    it.
    """
    if event_name in EVENT_CLASSES:
        return EVENT_CLASSES[event_name]

    for regexp, cls in EVENT_WILDCARDS:
        if regexp.match(event_name):
            return cls

    return GameEvent

def create_game_event(stream_binding, data):
    """
    Creates a new GameEvent object from a stream binding and the un-humanized game
    event data.
    """
    event_list = stream_binding.prologue.game_event_list
    name, properties = game_event.humanize(data, event_list)

    cls = find_game_event_class(name)

    return cls(stream_binding=stream_binding, name=name, properties=properties)

class GameEvent(object):
    """
    Base class for all game events. Handles humanise and related things.
    """

    def __init__(self, stream_binding, name, properties):
        # Note that game events can't really be tracked across ticks, so
        # we just pass the data

        self.name = name
        """
        The name of the GameEvent. i.e. ``"dota_combatlog"``, ``"dota_chase_hero"``.
        """
        self.properties = properties

        self.stream_binding = stream_binding

    def __repr__(self):
        return "{}({})".format(self.name, self.properties)
