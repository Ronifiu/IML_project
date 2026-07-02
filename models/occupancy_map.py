import numpy as np
from constants import OccupancyMapConfig, RewardConfig


class OccupancyMap:

    UNKNOWN = OccupancyMapConfig.UNKOWN
    FREE = OccupancyMapConfig.FREE
    BLOCKED = OccupancyMapConfig.BLOCKED

    ACTIONS = OccupancyMapConfig.ACTIONS

    def __init__(self):
        self.tiles = {}
        self.visit_counts = {}
        self.visited_maps = set()
        self.visited_warp_tiles = set()

    def clear(self):
        self.tiles.clear()
        self.visit_counts.clear()
        self.visited_maps.clear()
        self.visited_warp_tiles.clear()

    def mark_visit(self, map_id, x, y):
        key = (map_id, x, y)
        self.visit_counts[key] = self.visit_counts.get(key, 0) + 1

    def get_visit_count(self, map_id, x, y):
        return self.visit_counts.get((map_id, x, y), 0)
    

    def mark_free(self, map_id, x, y):
        self.tiles[(map_id, x, y)] = self.FREE

    def mark_blocked(self, map_id, x, y):
        self.tiles[(map_id, x, y)] = self.BLOCKED

    def get(self, map_id, x, y):
        return self.tiles.get(
            (map_id, x, y),
            self.UNKNOWN
        )
    
    
    def visit_map(self, map_id):
        if map_id not in self.visited_maps:
            self.visited_maps.add(map_id)
            return True

        return False


    def has_visited_map(self, map_id):
        return map_id in self.visited_maps


    def visited_map_count(self):
        return len(self.visited_maps)

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

        self.mark_visit(new_map, new_x, new_y)
        self.visit_map(new_map)

        # map changed (door/building)
        if old_map != new_map:
            return

        dx, dy = self.ACTIONS.get(action.value, (0, 0))

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

    def mark_warp_rewarded(self, map_id, x, y):
        self.visited_warp_tiles.add((map_id, x, y))

    def is_warp_rewarded(self, map_id, x, y):
        return (map_id, x, y) in self.visited_warp_tiles

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