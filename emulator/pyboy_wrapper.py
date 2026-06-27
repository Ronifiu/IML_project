from pyboy import PyBoy
from constants import Action, ACTION_MAP

class PyBoyWrapper:
    def __init__(self, rom_path, frame_skip = 4):
        self.pyboy = PyBoy(rom_path)
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