class StreamBinding(object):
  # Just another layer of indirection
  world = None
  tick = None

  def __init__(self, demo, start_tick=5000):
    self.demo = demo
    self.go_to_tick(start_tick)

  def iter_ticks(self, start=None, end=None, step=1):
    if start is None:
      start = self.tick
    if end is not None:
      assert start < end

    last_tick = start - step - 1
    for tick, _, world in self.demo.stream(tick=start):
      if end is not None and tick >= end:
        break

      if tick - last_tick < step:
        continue
      else:
        last_tick = tick

      self.tick = tick
      self.world = world
      yield tick

  def __iter__(self):
    return self.iter_ticks()

  @property
  def players(self):
    from . import Player

    return [p for p in Player.get_all(self) if
            p.index != None and p.team != "spectator"]

  @property
  def rules(self):
    from .gamerules import GameRules
    rules = GameRules.get_all(self)
    assert len(rules) == 1
    return rules[0]

  def go_to_tick(self, tick):
    for tick, _, world in self.demo.stream(tick=tick):
      self.tick = tick
      self.world = world
      return

  @staticmethod
  def from_file(filename, *args, **kwargs):
    from skadi.replay import demo as rd
    import io

    f = io.open(filename, "r+b")
    demo = rd.construct(f)
    return StreamBinding(demo, *args, **kwargs)
