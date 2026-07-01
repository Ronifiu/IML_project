from pyboy import PyBoy

pyboy = PyBoy("roms/Pokemon_Red.gb")
pyboy.set_emulation_speed(1)

while True:
    pyboy.tick()