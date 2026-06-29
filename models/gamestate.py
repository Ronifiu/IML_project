from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class GameState:
    x: int
    y: int
    map_id: int
    direction: int
    hp: int
    in_battle: bool

    def to_numpy(self):
        return np.array([
            self.x,
            self.y,
            self.map_id,
            self.direction,
            self.hp,
            self.in_battle,
        ], dtype=np.float32)

    @property
    def tile(self):
        return (self.map_id, self.x, self.y)