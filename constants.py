from enum import Enum

"""
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    B = 5
    START = 6
    SELECT = 7
    NO_OP = 8

ACTION_MAP = {
    Action.UP: "up",
    Action.DOWN: "down",
    Action.LEFT: "left",
    Action.RIGHT: "right",
    Action.A: "a",
    Action.B: "b",
    Action.START: "start",
    Action.SELECT: "select",
}
"""
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    NO_OP = 5

ACTION_MAP = {
    Action.UP: "up",
    Action.DOWN: "down",
    Action.LEFT: "left",
    Action.RIGHT: "right",
    Action.A: "a",
}



MAX_STEPS = 1000

class RewardConfig:
    NEW_TILE = 10.0
    NEW_MAP = 20.0
    HP_LOSS = -5.0
    FRAME_TAX = -0.1

class AgentConfig:
    GAMMA = 0.99
    EPSILON = 0.3
    MIN_EPSILON = 0.05
    EPSILON_DECAY = 0.995
    LR = 1e-3

class ReplayBufferConfig:
    BUFFER_SIZE = 50000
    BATCH_SIZE = 64

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