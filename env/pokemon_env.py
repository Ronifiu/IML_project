import gymnasium as gym
from gymnasium import spaces
from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action, MAX_STEPS, RewardConfig
import numpy as np
from models.logger import EpisodeLogger
from models.gamestate import GameState

class PokemonEnv(gym.Env):
    def __init__(self, rom_path, debug=False, frame_skip=4):
        super().__init__()
        self.emulator = PyBoyWrapper(rom_path, debug, frame_skip)
        self.logger = EpisodeLogger()
        self.debug = debug
        self.frame_skip = frame_skip

        self.steps = 0
        self.previous_state = None
        self.visited = set()
        self.episode_num = 0
        self.episode_reward = 0

        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(7,),
            dtype=np.float32
        )

    def reset(self, *, seed=None, options=None):
        if self.steps > 0:
            self.logger.save(f"logs/episode_{self.episode_num}.csv")

        super().reset(seed=seed)
        self.emulator.reset()

        self.steps = 0
        self.visited.clear()
        obs = self.get_observation()
        self.previous_state = None
        self.episode_reward = 0

        self.logger.clear()

        return obs, {}

    def step(self, action):
        self.previous_state = self.get_state()
        action = Action(action)

        self.emulator.step(action)
        obs = self.get_observation()
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

        return obs, reward, terminated, truncated, {}


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
            reward -= RewardConfig.HP_LOSS

        
        return reward

    def get_observation(self):
        state = self.get_state()
        return state.to_numpy()
    
    def get_player_position(self):
        x, y = self.emulator.get_player_position()
        return (x, y)
    
    def get_mapID(self):
        map_id = self.emulator.get_mapID()
        return map_id
    
    def get_current_health(self):
        health = self.emulator.get_current_health()
        return health
    
    def get_battle_state(self):
        battle_state = self.emulator.get_battle_state()
        return battle_state
    
    def get_player_direction(self):
        player_direction = self.emulator.get_player_direction()
        return player_direction
    
    def get_state(self):
        return self.emulator.get_state()
    