import gymnasium as gym
from gymnasium.wrappers import FrameStackObservation
import torch
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from env.pokemon_env import PokemonEnv
from dqn.agent import Agent
from constants import AgentConfig

# Setup Environment
env = PokemonEnv('roms/Pokemon_Red.gb', debug=False, frame_skip=24, render=True)
num_frames = 4
env = FrameStackObservation(env, stack_size=num_frames)
action_dim = env.action_space.n

# Setup Agent
agent = Agent(input_channels=num_frames, action_dim=action_dim)

# 2. Initialize TensorBoard Writer
writer = SummaryWriter(log_dir="runs/pokemon_experiment_1")

episodes = 500
print(f"Starting training on device: {agent.device}")

try:
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        total_reward = 0
        steps = 0

        while not done:
            action = agent.choose_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            total_reward += reward
            steps += 1

            agent.replay_buffer.add(np.array(state), action, reward, np.array(next_state), done)
            agent.train() 
            state = next_state

        # Decay epsilon
        agent.epsilon = max(AgentConfig.MIN_EPSILON, agent.epsilon * AgentConfig.EPSILON_DECAY)
        
        # 3. Log metrics to TensorBoard
        writer.add_scalar("Reward/Episode_Total", total_reward, episode)
        writer.add_scalar("Stats/Steps_Taken", steps, episode)
        writer.add_scalar("Stats/Epsilon", agent.epsilon, episode)
        
        print(f"Episode {episode + 1} | Steps: {steps} | Reward: {total_reward:.2f} | Epsilon: {agent.epsilon:.3f}")

        if (episode + 1) % 50 == 0:
            torch.save(agent.model.state_dict(), f"saves/pokemon_dqn_ep{episode+1}.pth")
            print(f"*** Model checkpoint saved at episode {episode+1} ***")

except KeyboardInterrupt:
    print("\nTraining interrupted by user.")
    torch.save(agent.model.state_dict(), "saves/pokemon_dqn_interrupted.pth")

finally:
    env.close()
    writer.close() # 4. Close the writer properly