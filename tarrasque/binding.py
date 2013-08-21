
class StreamBinding(object):
  # Just another layer of indirection
  world = None
  tick = None

  def __init__(self, demo, start_tick=5000):
    self.demo = demo
    self.go_to_tick(start_tick)

  def iter_ticks(self, start=None, end=None):
    if start is None:
      start = self.tick
    if end is not None:
      assert start < end

    for tick, _, world in self.demo.stream(tick=start):
      if end is not None and tick >= end:
        break

      self.tick = tick
      self.world = world
      yield tick

  def __iter__(self):
    return self.iter_ticks()

  @property
  def players(self):
    from . import Player

    players = []
    player_resource_dt = "DT_DOTA_PlayerResource"
    ehandle, player_resource = self.world.find_by_dt(player_resource_dt)

    # Player resource arrays have 32 elements
    for index in range(32):
      name = player_resource[("m_iszPlayerNames", "%04d" % index)]
      if name == "":
        break

      player = Player(stream_binding=self, ehandle=ehandle, index=index)
      players.append(player)
    return players

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