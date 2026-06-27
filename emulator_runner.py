from pyboy import PyBoy
pyboy = PyBoy('roms/Pokemon_Red.gb')
while pyboy.tick():
    pass
pyboy.stop()
