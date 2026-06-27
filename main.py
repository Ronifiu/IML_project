from emulator.pyboy_wrapper import PyBoyWrapper
from constants import Action

emu = PyBoyWrapper('roms/Pokemon_Red.gb')

emu.tick(60)

image = emu.get_screen()

image.save('screenshots/screen.png')



emu.tick(600)
emu.press('a')
image = emu.get_screen()
image.save('screenshots/screen1apress.png')

emu.tick(300)
emu.press('a')
image = emu.get_screen()
image.save('screenshots/screen2apress.png')

emu.tick(300)
emu.press('a')
image = emu.get_screen()
image.save('screenshots/screen3apress.png')


emu.close()