import pandas as pd

class EpisodeLogger:
    def __init__(self):
        self.records = []

    def clear(self):
        self.records.clear()

    def log(self, step, action, state, reward, visited, terminated, truncated, episode_reward):
        self.records.append({
            "step": step,
            "action": action,
            "x": state.x,
            "y": state.y,
            "map": state.map_id,
            "direction": state.direction,
            "hp": state.hp,
            "battle": state.in_battle,
            "reward": reward,
            "visited_tiles": visited,
            "terminated": terminated,
            "truncated": truncated,
            "episode_reward": episode_reward,
        })

    def save(self, filename):
        df = pd.DataFrame(self.records)
        df.to_csv(filename, index=False)