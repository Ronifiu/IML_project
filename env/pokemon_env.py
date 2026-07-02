import gymnasium as gym
import cv2
from gymnasium import spaces
from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action, MAX_STEPS, RewardConfig, OccupancyMapConfig, MAP_NAMES, MAX_BOREDOM_STEPS
import numpy as np
from models.logger import EpisodeLogger
from models.gamestate import GameState
from models.occupancy_map import OccupancyMap
from collections import deque

class PokemonEnv(gym.Env):
    def __init__(self, rom_path, debug=False, frame_skip=24, render=True):
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
        self.recent_actions = deque(maxlen=10)
        self.recent_maps = deque(maxlen=4)
        self.oak_reward_given = False
        self.steps_since_progress = 0
        self.is_done = False
        self.steps_in_current_map = 0

        self.action_space = spaces.Discrete(len(Action))

        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(84, 84), 
            dtype=np.uint8
        )

    def reset(self, *, state_file='saves/start.state', seed=None, options=None):
        if self.steps > 0:
            self.logger.save(f"logs/episode_{self.episode_num}.csv")
            self.logger.clear()
            self.episode_num += 1

        super().reset(seed=seed)
        self.emulator.load_state(state_file)
        self.emulator.tick(1)

        self.steps = 0
        self.visited.clear()
        self.occupancy.clear()
        self.recent_actions.clear()
        self.recent_maps.clear()
        state = self.get_state()
        self.previous_state = state
        self.episode_reward = 0
        self.oak_reward_given = False
        self.is_done = False
        self.steps_since_progress = 0
        self.steps_in_current_map = 0

        return self.get_observation(), {}

    def step(self, action):
        self.recent_actions.append(action)
        self.previous_state = self.get_state()
        action = Action(action)

        self.emulator.step(action)
        current_state = self.get_state()

        if current_state.map_id != self.previous_state.map_id:
            self.recent_maps.append(current_state.map_id)
            self.steps_in_current_map += 1

        reward = self.get_reward(current_state)
        self.episode_reward += reward
        self.steps += 1
        terminated = False
        if self.emulator.get_battle_state() > 0:
            terminated = True
            reward += 500
            print("Agent entered rival fight.")
        if self.is_done:
            terminated = True
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
        made_progress = False

        visits = self.occupancy.get_visit_count(state.map_id, state.x, state.y)
        if visits == 1:
            reward += RewardConfig.NEW_TILE
            made_progress = True

        if visits > 2:
            reward += min(visits, 10) * RewardConfig.REVISIT_PENALTY

        if self.occupancy.visit_map(state.map_id):
            reward += RewardConfig.NEW_MAP
            made_progress = True

        if len(self.recent_actions) == 10:
            if self.is_looping():
                reward += RewardConfig.LOOP_PENALTY

        if self.is_stuck():
            reward += RewardConfig.LOOP_PENALTY

        if state.pokemon_count > self.previous_state.pokemon_count:
            print("Starter Pokemon Selected.")
            reward += RewardConfig.POKEMON_CATCHED
            made_progress = True

        if self.is_on_warp_tile(state):
            if not self.occupancy.is_warp_rewarded(state.map_id, state.x, state.y):
                reward += RewardConfig.WARP_TILE_STEP
                self.occupancy.mark_warp_rewarded(state.map_id, state.x, state.y)
                made_progress = True

        if self.is_oak_cutscene(state):
            if getattr(self, 'oak_reward_given', False) == False:
                print("Oak cutscene reached.")
                reward += RewardConfig.OAK_CUTSCENE
                self.oak_reward_given = True
                made_progress = True

        if len(self.recent_maps) == 4:
            if self.recent_maps[0] == self.recent_maps[2] and self.recent_maps[1] == self.recent_maps[3]:
                reward += -5.0
                self.recent_maps.clear()

        if state.map_id == 37 and self.steps_in_current_map > 100:
            reward -= 0.5

        if made_progress:
            self.steps_since_progress = 0
        else:
            self.steps_since_progress += 1

        # If the agent hasn't done anything useful in 200 steps, kill the episode.
        if self.steps_since_progress >= MAX_BOREDOM_STEPS:
            print("Agent got bored (stuck/humping a wall). Terminating early.")
            self.is_done = True

            reward -= 100

        
        return reward

    def is_looping(self):
        # Checks if the last actions are just repeating a pattern
        # e.g., [Up, Down, Up, Down, Up, Down, Up, Down, Up, Down]
        acts = list(self.recent_actions)
        return (acts[0::2] == acts[2::2]) and (acts[1::2] == acts[3::2])
    
    def is_stuck(self):
        if len(self.recent_actions) < 10:
            return False
        return len(set(self.recent_actions)) == 1
    
    def get_state(self):
        return self.emulator.get_state()
    
    def get_observation(self):
            screen = self.emulator.get_screen()
            
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2GRAY)
            
            resized_screen = cv2.resize(
                gray_screen, 
                (84, 84), 
                interpolation=cv2.INTER_AREA
            )
            
            return resized_screen
    
    def get_pokemon_count(self):
        return self.emulator.get_pokemon_count()

    def is_on_warp_tile(self, state: GameState):
        if state.map_id in RewardConfig.WARP_TILES:
            return (state.x, state.y) in RewardConfig.WARP_TILES[state.map_id]
        return False
    
    def is_oak_cutscene(self, state: GameState):
        return state.map_id == 0 and state.y <= 1
    
