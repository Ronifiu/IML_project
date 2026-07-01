import gymnasium as gym
from gymnasium import spaces
from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action, MAX_STEPS, RewardConfig, OccupancyMapConfig
import numpy as np
from models.logger import EpisodeLogger
from models.gamestate import GameState
from models.occupancy_map import OccupancyMap

class PokemonEnv(gym.Env):
    def __init__(self, rom_path, debug=False, frame_skip=4, render=True):
        super().__init__()
        self.emulator = PyBoyWrapper(rom_path, debug, frame_skip, render)
        self.emulator.reset()
        self.logger = EpisodeLogger()
        self.occupancy = OccupancyMap()
        self.debug = debug
        self.frame_skip = frame_skip

        self.steps = 0
        self.previous_state = None
        self.visited = set()
        self.episode_num = 0
        self.episode_reward = 0

        self.action_space = spaces.Discrete(len(Action))

        sample_obs = self.get_observation()
        self.observation_space = spaces.Box(
            low=-1,
            high=1,
            shape=sample_obs.shape,
            dtype=np.float32
        )

    def reset(self, *, seed=None, options=None):
        if self.steps > 0:
            self.logger.save(f"logs/episode_{self.episode_num}.csv")
            self.logger.clear()
            self.episode_num += 1

        super().reset(seed=seed)
        self.emulator.reset()

        self.steps = 0
        self.visited.clear()
        state = self.get_state()
        self.previous_state = state
        self.episode_reward = 0

        return self.get_observation(), {}

    def step(self, action):
        self.previous_state = self.get_state()
        action = Action(action)

        self.emulator.step(action)
        current_state = self.get_state()

        reward = self.get_reward(current_state)
        self.episode_reward += reward
        self.steps += 1
        terminated = False
        truncated = self.steps >= MAX_STEPS


        self.logger.log(
            step=self.steps,
            action=action,
            state=current_state,
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            visited=len(self.visited),
            episode_reward=self.episode_reward,
        )
        self.occupancy.update(
            self.previous_state.map_id,
            self.previous_state.x,
            self.previous_state.y,
            action,
            current_state.map_id,
            current_state.x,
            current_state.y
        )

        return self.get_observation(), reward, terminated, truncated, {}


    def render(self):
        pass

    def close(self):
        self.emulator.close()

    def get_reward(self, state: GameState):
        reward = 0
        tile = state.tile
        if tile not in self.visited:
            reward += RewardConfig.NEW_TILE
            self.visited.add(tile)

        if state.map_id != self.previous_state.map_id:
            reward += RewardConfig.NEW_MAP

        if state.hp < self.previous_state.hp:
            reward += RewardConfig.HP_LOSS

        reward += RewardConfig.FRAME_TAX

        
        return reward
    
    def get_state(self):
        return self.emulator.get_state()
    
    def get_observation(self):
        state = self.get_state()

        local = self.occupancy.local_view(
            state.map_id,
            state.x,
            state.y,
            radius=OccupancyMapConfig.RADIUS
        )

        obs = np.concatenate([
            state.to_numpy(),
            local
        ])

        return obs.astype(np.float32)