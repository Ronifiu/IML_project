import random
import torch
import torch.nn as nn
import torch.optim as optim
from constants import AgentConfig, ReplayBufferConfig
from dqn.dqn import DQN
from dqn.replay import ReplayBuffer
import copy
import numpy as np

class Agent:
    def __init__(self, input_channels, action_dim, state_space):
        self.gamma = AgentConfig.GAMMA
        self.epsilon = AgentConfig.EPSILON
        self.action_dim = action_dim

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps") # For Apple Silicon
        else:
            self.device = torch.device("cpu")
            print("Warning: Training a CNN on CPU will be very slow.")

        self.model = DQN(input_channels, action_dim).to(self.device)

        # Target network:
        self.target_model = copy.deepcopy(self.model).to(self.device)
        self.target_model.eval()

        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=AgentConfig.LR
        )

        self.criterion = nn.SmoothL1Loss()

        self.replay_buffer = ReplayBuffer(ReplayBufferConfig.BUFFER_SIZE, state_shape=state_space)
        self.batch_size = ReplayBufferConfig.BATCH_SIZE

        self.target_update = 1000
        self.train_steps = 0
        self.episode_trajectory = []

    def preprocess_state(self, state):
        """Helper to handle dimensions and normalization"""
        # Convert to numpy array in case it's a LazyFrames object from Gym
        state = np.array(state)
        
        # PyTorch expects [Batch, Channels, Height, Width]
        # If your state comes in as [Height, Width, Channels], permute it here:
        if state.shape[-1] == 4: # Assuming 4 stacked frames
            state = np.transpose(state, (2, 0, 1))
            
        # Convert to tensor, add batch dimension, move to device, and normalize
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        return state_tensor / 255.0

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        
        # Preprocess the state (normalize and move to GPU)
        state_tensor = self.preprocess_state(state)

        with torch.no_grad():
            q_values = self.model(state_tensor)

        return torch.argmax(q_values).item()
    
    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = \
            self.replay_buffer.sample(self.batch_size)

        # 3. Process the batch (Handle dimensions, move to GPU, normalize)
        # Assuming ReplayBuffer outputs [Batch, Height, Width, Channels]
        # We need to reshape to [Batch, Channels, Height, Width]
        if states.shape[-1] == 4: 
            states = np.transpose(states, (0, 3, 1, 2))
            next_states = np.transpose(next_states, (0, 3, 1, 2))

        # Convert to tensors, move to device, and normalize pixel values (0-255 -> 0.0-1.0)
        states = torch.FloatTensor(states).to(self.device) / 255.0
        next_states = torch.FloatTensor(next_states).to(self.device) / 255.0
        
        # Standard tensor conversions for the rest
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        current_q = self.model(states).gather(1, actions).squeeze(1)

        with torch.no_grad():
            next_q = self.target_model(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)

        loss = self.criterion(current_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        
        self.optimizer.step()

        self.train_steps += 1

        if self.train_steps % self.target_update == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        return loss

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add(state, action, reward, next_state, done)
        
        self.episode_trajectory.append((state, action, reward, next_state, done))

        if reward >= 100.0:
            winning_path = self.episode_trajectory[-200:]
            print(f"Massive win ({reward})! Force memorizing the last {len(winning_path)} steps...")
            
            for _ in range(5):
                for step_data in winning_path:
                    self.replay_buffer.add(*step_data)

        if done:
            self.episode_trajectory = []