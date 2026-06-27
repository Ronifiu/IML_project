from enum import Enum

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