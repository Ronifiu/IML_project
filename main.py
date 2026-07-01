from env.pokemon_env import PokemonEnv
from dqn.agent import Agent
from constants import AgentConfig

env = PokemonEnv('roms/Pokemon_Red.gb', debug=False, frame_skip=16, render=True)

state_dim = len(env.reset()[0])
action_dim = env.action_space.n

agent = Agent(state_dim, action_dim)

episodes = 25

for episode in range(episodes):
    state, _ = env.reset()

    done = False

    while not done:
        action = agent.choose_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        try:
            agent.replay_buffer.add(
                state,
                action,
                reward,
                next_state,
                done
            )
            agent.train()
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            env.emulator.close()
            env.close()
            done = True

        state = next_state
    agent.epsilon = max(AgentConfig.MIN_EPSILON, agent.epsilon * AgentConfig.EPSILON_DECAY)
    print(f"episode {episode} is completed")
env.reset()