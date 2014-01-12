import collections
import warnings

import skadi.state.match as stt_mtch
import skadi.demo

from protobuf.impl import demo_pb2 as pb_d

class StreamBinding(object):
    """
    The StreamBinding class is Tarrasque's metaphor for the replay. Every
    Tarrasque entity class has a reference to an instance of this
    class, and when the tick of the instance changes, the data returned by
    those classes changes. This makes it easy to handle complex object graphs
    without explicitly needing to pass the Skadi demo object around.

    .. note:: Where methods on this class take absolute tick values (i.e. the
       ``start`` and ``end`` arguments to :meth:`iter_ticks`), special string
       arguments may be passed. These are:

       * ``"start"`` - The start of the replay
       * ``"draft"`` - The start of the draft
       * ``"pregame"`` - The end of the draft phase
       * ``"game"`` - The time when the game clock hits 0
       * ``"postgame"`` - The time the ancient is destroyed
       * ``"end"`` - The last tick in the replay

       These values will not be 100% accurate, but should be good +-50 ticks
    """

    @property
    def user_messages(self):
        """
        The user messages for the current tick.
        """
        return self._user_messages

    @property
    def game_events(self):
        """
        The game events in the current tick.
        """
        from .gameevents import create_game_event

        events = []
        for data in self._game_events:
            events.append(create_game_event(stream_binding=self, data=data))
        return events

    # Just another layer of indirection
    # These are properties for autodoc reasons mostly
    @property
    def entities(self):
        """
        Entities for the current tick.
        """
        return self.snapshot.entities

    @property
    def snapshot(self):
        """
        The most recent snapshot.
        """
        return self._match.snapshots[-1]

    @property
    def tick(self):
        """
        The current tick.
        """
        return self.snapshot.tick

    @property
    def demo(self):
        """
        The Skadi DemoIO object that the binding is reading from.
        """
        return self._demo

    @property
    def modifiers(self):
        """
        The Skadi modifiers object for the tick.
        """
        return self.snapshot.modifiers

    @property
    def string_tables(self):
        """
        The string_table provided by Skadi.
        """
        return self.snapshot.string_tables

    @property
    def prologue(self):
        """
        The prologue of the replay.
        """
        return self._prologue

    @property
    def epilogue(self):
        """
        The epilogue of the replay.
        """
        return self._epilogue

    def __init__(self, demo, start="game"):
        import skadi.index.prologue
        import skadi.index.epilogue

        self._demo = demo
        self._user_messages = []
        self._game_events = []

        gio = demo.bootstrap()
        self._prologue = skadi.index.prologue.parse(demo)

        self._demo_start = demo.handle.tell()

        demo.handle.seek(gio)
        self._epilogue = skadi.index.epilogue.parse(demo)

        self.reset()

        self._populate_state_change_times()

        if isinstance(start, basestring):
            self.go_to_state_change(start)
        elif isinstance(start, int):
            self.go_to_tick(start)
        elif isinstance(start, float):
            self.go_to_time(start)
        else:
            raise ValueError("Invalid start type")

    def _populate_state_change_times(self):
        """
        Moves to the end of the replay and populates the _state_change_times dict.
        """
        self.go_to_tick(self._epilogue.playback_ticks - 2)

        self._state_change_times = {
            "draft": self.info.draft_start_time,
            "pregame": self.info.pregame_start_time,
            "game": self.info.game_start_time,
            "postgame": self.info.game_end_time
        }

    def reset(self, pos=0):
        self._demo.handle.seek(self._demo_start)

        fps, ps = skadi.demo.preroll(self._demo, pos)
        
        self._match = stt_mtch.mk(self._prologue, fps, ps)

    def advance_tick(self):
        for peek, message in self.demo:
            if peek.kind == pb_d.DEM_FullPacket:
                continue
            elif peek.kind != pb_d.DEM_Packet:
                assert peek.kind != pb_d.DEM_Stop
                return False
            pb = pb_d.CDemoPacket()
            pb.ParseFromString(message)
            self._match.snapshot(peek.tick, pb.data)

    def advance_full_tick(self):
        for peek, _ in self.demo:
            if peek.kind == pb_d.DEM_FullPacket:
                break
        return self.advance_tick()

    def go_to_tick(self, tick):
        """
        Moves to the given tick, or the next tick after it. Returns the tick moved
        to.
        """
        self.reset(tick)

        return self.tick

    def iter_ticks(self, start=None, end=None, step=1):
        """
        A generator that iterates through the demo's ticks and updates the
        :class:`StreamBinding` to that tick. Yields the current tick.

        The start parameter defines the tick to iterate from, and if not set, the
        current tick will be used instead.

        The end parameter defines the point to stop iterating; if not set,
        the iteration will continue until the end of the replay.

        The step parameter is the number of ticks to consume before yielding
        the tick; the default of one means that every tick will be yielded. Do
        not assume that the step is precise; the gap between two ticks will
        always be larger than the step, but usually not equal to it.
        """
        if start is not None:
            self.go_to_tick(start)

        if end is None:
            end = self._state_change_ticks["end"]

        self._user_messages = []
        self._game_events = []

        last_tick = self.tick - step - 1
        while self.advance_tick():

            if isinstance(end, str):
                if self.info.game_state == end:
                    break
            elif isinstance(end, float):
                if self.info.game_time < end:
                    break
            else:
                if self.tick >= end:
                    break

            self._user_messages.extend(self._stream.user_messages)
            self._game_events.extend(self._stream.game_events)

            if self.tick - last_tick < step:
                continue
            else:
                last_tick = self.tick

            yield self.tick

            self._user_messages = []
            self._game_events = []

    def iter_full_ticks(self, start=None, end=None):
        """
        A generator that iterates through the demo's 'full ticks'; sync points
        that occur once a minute. Should be _much_ faster than
        :method:`iter_ticks`.

        The ``start`` argument may take the same range of values as the ``start``
        argument of :method:`iter_ticks`. The first full tick yielded will be the
        next full tick after the position obtained via `self.go_to_tick(start)`.
         The end tick may either be a tick value or a game state. The last full
        tick yielded will be the first full tick after the tick value/game state
        change.
        """
        if start is not None:
            self.go_to_tick(start)

        for _ in self._stream.iterfullticks():
            if end:
                if isinstance(end, basestring):
                    if self.info.game_state == end:
                        break
                else:
                    if self.tick > end:
                        break
            self._user_messages = []
            self._game_events = []
            yield self.tick

        self._user_messages = (self._stream.user_messages or [])[:]
        self._game_events = (self._stream.game_events or [])[:]

        yield self.tick

    def go_to_time(self, time):
        """
        Moves to the tick with the given game time. Could potentially overshoot,
        but not by too much. Will not undershoot.

        Returns the tick it has moved to.
        """
        raise NotImplemented()
        # Go for 31 tps as would rather exit FP loop earlier than
        # sooner. 1.5 for same reason
        FP_REGION = 1800 * 1.5 / 31

        # If the time we're going to is behind us, recreate the stream
        if time < self.info.game_time:
            self._match = stt_mtch.mk(self._prologue)

        # If the time is more than 1.5 full packets ahead of us, iter full ticks
        if time > self.info.game_time + FP_REGION:
            while self.info.game_time + FP_REGION > time and\
                  self.info.game_time < time:
                # Apply the next full packet
                pass

        for _ in self._stream:
            if self.info.game_time > time:
                break
        else:
            raise IndexError("Time {} out of range".format(time))

        self._user_messages = self._stream.user_messages[:]
        self._game_events = self._stream.game_events[:]
        return self.tick

    def go_to_state_change(self, state):
        """
        Moves to the time when the :attr:`GameInfo.game_state` changed to the given
        state. Valid values are equal to the possible values of
        :att:`~GameInfo.game_state`, along with ``"start"`` and ``"end"`` which
        signify the first and last tick in the replay, respectively.

        Returns the tick moved to.
        """
        if state in self._state_change_ticks:
            return self.go_to_tick(self._state_change_ticks[state])
        elif state in self._state_change_times:
            return self.go_to_time(self._state_change_times[state])
        else:
            raise ValueError("Unsupported state {}".format(repr(state)))

    def __iter__(self):
        return self.iter_ticks()

    @property
    def players(self):
        """
        A list of :class:`Player` objects, one for each player in the game.
        This excludes spectators and other non-hero-controlling players.
        """
        from . import Player

        return sorted([p for p in Player.get_all(self) if
                       p.index != None and p.team != "spectator"],
                       key=lambda p:p.index)

    @property
    def info(self):
        """
        The :class:`GameInfo` object for the replay.
        """
        from .gameinfo import GameInfo
        info = GameInfo.get_all(self)
        assert len(info) == 1
        return info[0]

    @property
    def creeps(self):
        """
        The :class:`CreepManager` object for the replay.
        """
        from .creeps import CreepManager

        return CreepManager(self)

    @property
    def buildings(self):
        """
        The :class:`BuildingManager` object for the replay.
        """
        from .buildings import BuildingManager
        return BuildingManager(self)

    @staticmethod
    def from_file(filename, *args, **kwargs):
        """
        Loads the demo from the filename, and then initialises the
        :class:`StreamBinding` with it, along with any other passed arguments.
        """
        import skadi.io.demo

        with open(filename, "rb") as demo_file:
            demo_io = skadi.io.demo.mk(demo_file)

            return StreamBinding(demo_io, *args, **kwargs)
