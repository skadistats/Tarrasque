# This value is used to report None
NEGATIVE = 2 ** 21 - 1 # 2097151

# Map between integers and teams
TEAM_VALUES = {
  2: "radiant",
  3: "dire",
  5: "spectator",
  0: None,
}

WINNER_VALUES = {
    2: "radiant",
    3: "dire",
    5: None
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

GAME_MODE_VALUES = {
    0: "none",
    1: "all pick",
    2: "captain's mode",
    3: "random draft",
    4: "single draft",
    5: "all random",
    6: "intro",
    7: "diretide",
    8: "reverse captain's mode",
    9: "greeviling",
    10: "tutorial",
    11: "mid only",
    12: "least played",
    13: "new player pool",
    14: "compendium matchmaking"
}

def generate_pick_values():
    b = "ban"
    p = "pick"
    return {
        1: "all pick",
        2: "single draft",
        4: "random draft",
        27: "all random",

        # CM values
        6: (b, 1),
        7: (b, 2),
        8: (b, 3),
        9: (b, 4),
        16: (p, 1),
        17: (p, 2),
        18: (p, 3),
        19: (p, 4),
        10: (b, 5),
        11: (b, 6),
        12: (b, 7),
        13: (b, 8),
        20: (p, 5),
        21: (p, 6),
        22: (p, 7),
        23: (p, 8),
        14: (b, 9),
        15: (b, 10),
        24: (p, 9),
        25: (p, 10),
        26: "complete"
    }

PICK_VALUES = generate_pick_values()

COMBAT_LOG_TYPES = {
    0: "damage",
    1: "heal",
    2: "modifier added",
    3: "modifier removed",
    4: "death"
}