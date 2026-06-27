import gymnasium as gym
from gymnasium import spaces
from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action
import numpy as np

class PokemonEnv(gym.Env):
    def __init__(self, rom_path, debug=False, frame_skip=4):
        super().__init__()
        self.emulator = PyBoyWrapper(rom_path, debug, frame_skip)
        self.debug = debug
        self.frame_skip = frame_skip

        self.reward = 0

        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(144,160,3),
            dtype=np.uint8
        )

    def reset(self, *, seed=None, options=None):
        self.emulator.reset()
        obs = np.array(self.emulator.get_screen())

        return obs, {}

    def step(self, action):
        action = Action(action)

        self.emulator.step(action)
        obs = np.array(self.emulator.get_screen())

        reward = 0
        terminated = False
        truncated = False
        info = {}

        return obs, reward, terminated, truncated, info


    def render(self):
        pass

    def close(self):
        self.emulator.close()