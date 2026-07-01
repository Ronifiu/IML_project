from env.pokemon_env import PokemonEnv
from constants import Action

env = PokemonEnv("roms/Pokemon_Red.gb", debug=True, frame_skip=16)

env.reset()

env.emulator.tick(60)
env.step(Action.RIGHT)
env.emulator.tick(60)
env.step(Action.RIGHT)
env.emulator.tick(60)
env.step(Action.RIGHT)
env.emulator.tick(60)
print("hello")
env.step(Action.RIGHT)
env.emulator.tick(60)
env.step(Action.LEFT)
env.emulator.tick(60)
env.step(Action.LEFT)
env.emulator.tick(60)
env.step(Action.LEFT)
env.emulator.tick(60)
env.step(Action.LEFT)
env.emulator.tick(60)
env.step(Action.LEFT)
env.emulator.tick(60)


env.reset()
env.close()