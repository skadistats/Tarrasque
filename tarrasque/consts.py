# This value is used to report None
NEGATIVE = 2 ** 21 - 1 # 2097151

# Map between integers and teams
TEAM_VALUES = {
  2: "radiant",
  3: "dire",
  5: "spectator",
  0: None,
}

LIFE_STATE_VALUES = {
  0: "alive",
  1: "dying",
  2: "dead",
  3: "respawnable",
  4: "discardbody"
}

GAME_STATE_VALUES = {
  1: "loading",
  2: "draft",
  4: "pregame",
  5: "game",
  6: "postgame"
}