from pyboy import PyBoy
from constants import Action, ACTION_MAP
from models.gamestate import GameState
import cv2


class PyBoyWrapper:
    def __init__(self, rom_path, debug=False, frame_skip=24, render=True):
        self.pyboy = PyBoy(rom_path, sound_emulated=False)
        self.debug = debug
        self.render = render
        if not self.debug:
            self.pyboy.set_emulation_speed(0)
            print("Unlimited speed enabled")
        else:
            self.pyboy.set_emulation_speed(1)
            print("Debug mode")
        self.frame_skip = frame_skip

    def tick(self, frames=1):
        if self.debug:
            for _ in range(frames):
                self.pyboy.tick(1, render=self.render)
        else:
            self.pyboy.tick(frames, render=self.render)


    def get_screen(self):
        return self.pyboy.screen.ndarray
    
    def save_screen(self, path):
            screen = self.get_screen()
            screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
            cv2.imwrite(path, screen_bgr)
    
    def tap(self, action: Action):
        if action == Action.NO_OP:
            self.tick(self.frame_skip)
            return
        
        press_event, release_event = ACTION_MAP[action]
        
        self.pyboy.send_input(press_event)
        
        self.tick(16)
        
        self.pyboy.send_input(release_event)

        self.tick(self.frame_skip - 16)

    def step(self, action: Action):
        self.tap(action)


    def save_state(self, path):
        with open(path, 'wb') as f:
            self.pyboy.save_state(f)

    def load_state(self, path):
        with open(path, 'rb') as f:
            self.pyboy.load_state(f)

    def reset(self):
        self.load_state('saves/start.state')
        self.tick(1)
    
    def close(self):
        self.pyboy.stop(save=False)

    def get_player_position(self):
        player_x = self.pyboy.memory[0xD362]
        player_y = self.pyboy.memory[0xD361]
        return player_x, player_y

    def get_mapID(self):
        map_id = self.pyboy.memory[0xD35E]
        return map_id

    def get_current_health(self):
        health = self.pyboy.memory[0xD163]
        return health

    def get_battle_state(self):
        battle_state = self.pyboy.memory[0xD057]
        return battle_state
    
    def get_player_direction(self):
        player_direction = self.pyboy.memory[0xC109]
        return player_direction / 4
    
    def get_pokemon_count(self):
        return self.pyboy.memory[0xD163]
    
    def get_state(self):
        player_x, player_y = self.get_player_position()
        return GameState(
            x=player_x,
            y=player_y,
            map_id=self.get_mapID(),
            direction=self.get_player_direction(),
            hp=self.get_current_health(),
            in_battle=self.get_battle_state(),
            pokemon_count=self.get_pokemon_count(),
        )