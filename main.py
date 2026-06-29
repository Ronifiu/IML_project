from env.pokemon_env import PokemonEnv

env = PokemonEnv('roms/Pokemon_Red.gb', debug=True, frame_skip=4)

obs, info = env.reset()

for _ in range(100):

    action = env.action_space.sample()

    env.step(action)

env.reset()