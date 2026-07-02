from enum import Enum
from pyboy.utils import WindowEvent


MAX_BOREDOM_STEPS = 300
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    B = 5
    NO_OP = 6

ACTION_MAP = {
    Action.UP: (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP),
    Action.DOWN: (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN),
    Action.LEFT: (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT),
    Action.RIGHT: (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT),
    Action.A: (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
    Action.B: (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
}



MAX_STEPS = 3000

class RewardConfig:
    WARP_TILES = {
        37: [(7, 1)],               # Bedroom stairs
        36: [(2, 7), (3, 7)],       # Downstairs front door
        0:  [(12, 11), (13, 11)],   # Oak's lab entrance door
    }

    PALLET_TOWN_MAP_ID = 0
    OAKS_LAB_MAP_ID = 40

    NEW_TILE = 1.0
    NEW_MAP = 50.0
    HP_LOSS = -5.0
    REVISIT_PENALTY = -0.01
    LOOP_PENALTY = -2.0
    POKEMON_CATCHED = 200.0
    WARP_TILE_STEP = 10.0
    OAK_CUTSCENE = 150.0

class AgentConfig:
    GAMMA = 0.99
    EPSILON = 1.0
    MIN_EPSILON = 0.05
    EPSILON_DECAY = 0.97
    LR = 1e-4

class ReplayBufferConfig:
    BUFFER_SIZE = 100000
    BATCH_SIZE = 256

class OccupancyMapConfig:
    RADIUS = 1
    UNKOWN = -1.0
    FREE = 0.0
    BLOCKED = 1.0
    ACTIONS = {
        0: (0, -1),
        1: (0, 1),
        2: (-1, 0),
        3: (1, 0),
        4: (0, 0),
        5: (0, 0),
    }

MAP_NAMES = {
    0: "Pallet Town",
    1: "Viridian City",
    2: "Pewter City",
    3: "Cerulean City",
    4: "Lavender Town",
    5: "Vermilion City",
    6: "Celadon City",
    7: "Fuchsia City",
    8: "Cinnabar Island",
    9: "Pokémon League",
    10: "Saffron City",
    11: "Unused Fly Location",
    12: "Route 1",
    13: "Route 2",
    14: "Route 3",
    15: "Route 4",
    16: "Route 5",
    17: "Route 6",
    18: "Route 7",
    19: "Route 8",
    20: "Route 9",
    21: "Route 10",
    22: "Route 11",
    23: "Route 12",
    24: "Route 13",
    25: "Route 14",
    26: "Route 15",
    27: "Route 16",
    28: "Route 17",
    29: "Route 18",
    30: "Sea Route 19",
    31: "Sea Route 20",
    32: "Sea Route 21",
    33: "Route 22",
    34: "Route 23",
    35: "Route 24",
    36: "Route 25",
    37: "Red's House 1F",
    38: "Red's House 2F",
    39: "Blue's House",
    40: "Professor Oak's Lab",
    41: "Viridian Pokémon Center",
    42: "Viridian Poké Mart",
    43: "Viridian School",
    44: "Viridian Nickname House",
    45: "Viridian Gym",
    46: "Diglett's Cave Entrance",
    47: "Route 2 Gate",
    48: "Oak's Aide House",
    49: "Route 2 Gate",
    50: "Viridian Forest Gate",
    51: "Viridian Forest",
    52: "Pewter Museum 1F",
    53: "Pewter Museum 2F",
    54: "Pewter Gym",
    55: "Pewter Nidoran House",
    56: "Pewter Poké Mart",
    57: "Pewter House",
    58: "Pewter Pokémon Center",
    59: "Mt. Moon 1F",
    60: "Mt. Moon B1F",
    61: "Mt. Moon B2F",
    62: "Cerulean Burgled House",
    63: "Cerulean Trade House",
    64: "Cerulean Pokémon Center",
    65: "Cerulean Gym",
    66: "Bike Shop",
    67: "Cerulean Poké Mart",
    68: "Route 4 Pokémon Center",
    69: "Cerulean Burgled House (Alt)",
    70: "Route 5 Saffron Gate",
    71: "Route 5 Underground Entrance",
    72: "Day Care",
    73: "Route 6 Saffron Gate",
    74: "Route 6 Underground Entrance",
    75: "Route 6 Underground Entrance (Alt)",
    76: "Route 7 Saffron Gate",
    77: "Route 7 Underground Entrance",
    78: "Unused Underground Entrance",
    79: "Route 8 Saffron Gate",
    80: "Route 8 Underground Entrance",
    81: "Rock Tunnel Pokémon Center",
    82: "Rock Tunnel B1F",
    83: "Power Plant",
    84: "Route 11 Gate 1F",
    85: "Diglett's Cave",
    86: "Route 11 Gate 2F",
    87: "Route 12 Gate",
    88: "Sea Cottage",
    89: "Vermilion Pokémon Center",
    90: "Pokémon Fan Club",
    91: "Vermilion Poké Mart",
    92: "Vermilion Gym",
    93: "Vermilion House",
    94: "Vermilion Harbor",
    95: "S.S. Anne 1F",
    96: "S.S. Anne 2F",
    97: "S.S. Anne 3F",
    98: "S.S. Anne B1F",
    99: "S.S. Anne Deck",
    100: "S.S. Anne Kitchen",
}