import gymnasium as gym
from gymnasium.wrappers import FrameStackObservation
import torch
from torch.utils.tensorboard import SummaryWriter
import numpy as np
from env.pokemon_env import PokemonEnv
from dqn.agent import Agent
from constants import AgentConfig, MAX_STEPS


env = PokemonEnv('roms/Pokemon_Red.gb', debug=False, frame_skip=24, render=True)

num_frames = 4
env = FrameStackObservation(env, stack_size=num_frames)

action_dim = env.action_space.n
state_space = env.observation_space.shape

agent = Agent(input_channels=num_frames, action_dim=action_dim, state_space=state_space)
experiment_num = 6
dir = f"runs/pokemon_experiment_{experiment_num}"

writer = SummaryWriter(log_dir=dir)


TOTAL_TRAINING_STEPS = 250_000
CHECKPOINT_INTERVAL = 25_000 # Save every 50k steps

total_steps = 0
episode_num = 0

try:
    while total_steps < TOTAL_TRAINING_STEPS:
        episode_num += 1
        
            
        state, _ = env.reset()
        done = False
        episode_reward = 0
        steps = 0
        total_loss = 0

        while not done:
            action = agent.choose_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            agent.remember(state, action, reward, next_state, done)
            loss = agent.train()
            if loss is not None:
                total_loss += loss
            
            state = next_state
            total_steps += 1
            steps += 1
            episode_reward += reward

            # --- Checkpoint Saving ---
            if total_steps % CHECKPOINT_INTERVAL == 0:
                torch.save(agent.model.state_dict(), f"saves/model_{experiment_num}_step_{total_steps}.pth")
                print(f"Checkpoint saved at {total_steps} steps.")

        writer.add_scalar("Reward/Episode_Total", episode_reward, episode_num)
        writer.add_scalar("Stats/Steps_Taken", steps, episode_num)
        writer.add_scalar("Stats/Epsilon", agent.epsilon, episode_num)
        writer.add_scalar("Stats/Average_Loss", total_loss / steps, episode_num)

        # Decay Epsilon
        previous_epsilon = agent.epsilon
        #agent.epsilon = max(AgentConfig.MIN_EPSILON, agent.epsilon * AgentConfig.EPSILON_DECAY)
        exploration_phase_steps = TOTAL_TRAINING_STEPS * 0.8
        agent.epsilon = max(AgentConfig.MIN_EPSILON, 1.0 - (total_steps / exploration_phase_steps))

        
        print(f"Ep {episode_num} | Total Steps: {total_steps} | Reward: {episode_reward:.2f} | Epsilon: {previous_epsilon:.2f}")

except KeyboardInterrupt:
    print("\nTraining interrupted by user.")
    torch.save(agent.model.state_dict(), "saves/pokemon_dqn_interrupted.pth")

finally:
    env.close()
    writer.close()