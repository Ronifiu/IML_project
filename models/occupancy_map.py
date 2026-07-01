import numpy as np
from constants import OccupancyMapConfig


class OccupancyMap:

    UNKNOWN = OccupancyMapConfig.UNKOWN
    FREE = OccupancyMapConfig.FREE
    BLOCKED = OccupancyMapConfig.BLOCKED

    ACTIONS = OccupancyMapConfig.ACTIONS

    def __init__(self):
        self.tiles = {}

    def clear(self):
        self.tiles.clear()

    def mark_free(self, map_id, x, y):
        self.tiles[(map_id, x, y)] = self.FREE

    def mark_blocked(self, map_id, x, y):
        self.tiles[(map_id, x, y)] = self.BLOCKED

    def get(self, map_id, x, y):
        return self.tiles.get(
            (map_id, x, y),
            self.UNKNOWN
        )

    def update(
        self,
        old_map,
        old_x,
        old_y,
        action,
        new_map,
        new_x,
        new_y,
    ):

        # mark current tile
        self.mark_free(new_map, new_x, new_y)

        # map changed (door/building)
        if old_map != new_map:
            return

        dx, dy = self.ACTIONS[action.value]

        if (old_x, old_y) == (new_x, new_y):

            # movement failed
            self.mark_blocked(
                old_map,
                old_x + dx,
                old_y + dy
            )

        else:

            # movement succeeded
            self.mark_free(
                old_map,
                new_x,
                new_y
            )

    def local_view(
        self,
        map_id,
        x,
        y,
        radius=3
    ):
        obs = []

        for yy in range(y-radius, y+radius+1):
            for xx in range(x-radius, x+radius+1):

                obs.append(
                    self.get(
                        map_id,
                        xx,
                        yy
                    )
                )

        return np.array(obs, dtype=np.float32)