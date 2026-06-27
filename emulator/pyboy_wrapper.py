from pyboy import PyBoy
from constants import Action, ACTION_MAP

class PyBoyWrapper:
    def __init__(self, rom_path, debug=False, frame_skip=4):
        self.pyboy = PyBoy(rom_path)
        self.debug = debug
        if not self.debug:
            self.pyboy.set_emulation_speed(0)
        self.frame_skip = frame_skip

    def tick(self, frames=1):
        for _ in range(frames):
            self.pyboy.tick()

    def get_screen(self):
        return self.pyboy.screen.image
    
    def save_screen(self, path):
        self.get_screen().save(path)
    
    def tap(self, action: Action):
        if action == Action.NO_OP:
            self.tick(self.frame_skip)
            return
        
        self.pyboy.button_press(ACTION_MAP[action])
        self.tick(2)
        self.pyboy.button_release(ACTION_MAP[action])
        self.tick(self.frame_skip - 2)

    def step(self, action: Action):
        self.tap(action)
        
        return self.get_screen()

    def save_state(self, path):
        with open(path, 'wb') as f:
            self.pyboy.save_state(f)

    def load_state(self, path):
        with open(path, 'rb') as f:
            self.pyboy.load_state(f)

    def reset(self):
        self.load_state('saves/start.state')
    
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