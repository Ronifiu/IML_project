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
            self.x / 255.0,
            self.y / 255.0,
            self.map_id / 255.0,
            self.direction / 3.0,
            self.hp / 255.0,
            float(self.in_battle),
        ], dtype=np.float32)

    @property
    def tile(self):
        return (self.map_id, self.x, self.y)