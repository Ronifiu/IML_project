from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action

emu = PyBoyWrapper('roms/Pokemon_Red.gb')

emu.reset()

emu.step(Action.DOWN)
emu.tick(60)
emu.step(Action.UP)
emu.tick(60)
emu.step(Action.LEFT)
emu.tick(60)
emu.step(Action.RIGHT)
emu.tick(60)
emu.step(Action.START)
emu.tick(60)
emu.step(Action.A)
emu.tick(60)
emu.step(Action.B)
emu.tick(60)
emu.step(Action.B)
emu.tick(60)

emu.save_state('saves/test1.state')
emu.step(Action.RIGHT)
emu.tick(60)
emu.load_state('saves/test1.state')


emu.tick(120)

emu.close()