import itertools, math
from tarrasque import *

replay = StreamBinding.from_file("./demo/PL.dem", 10000)

graphing_team = "radiant"

heroes = [player.hero for player in replay.players if
         player.team == graphing_team]
print "Graphing for team {}, players: {}".format(graphing_team,
                    ", ".join(hero.player.name for hero in heroes))

distance_data = []
tick_data = []

# Step 300 ticks (10 secs) at a time in an effort to speed things up
for tick in replay.iter_ticks(start=10000, step=300):
  # The info object contains the game state, among other things. It
  # goes from "loading" -> "draft" -> "pregame" -> "game" -> "postgame"
  if replay.info.game_state == "postgame":
    break

  total_distance = 0
  n = 0
  for hero1, hero2 in itertools.combinations(heroes, 2):
    if not hero1.is_alive or not hero2.is_alive:
      continue

    x1, y1 = hero1.position
    x2, y2 = hero2.position
    distance = math.sqrt(abs((x1 - x2) ** 2 + (y1 - y2) ** 2))

    total_distance += distance
    n += 1

  distance_data.append(distance/n)
  tick_data.append(tick)

import matplotlib.pyplot as plt

plt.plot(tick_data, distance_data)
plt.show()
plt.savefig("./output.png")