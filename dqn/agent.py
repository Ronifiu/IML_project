import random
import torch
import torch.nn as nn
import torch.optim as optim
from constants import AgentConfig, ReplayBufferConfig
from dqn.dqn import DQN
from dqn.replay import ReplayBuffer
import copy

class Agent:
    def __init__(self, state_dim, action_dim):
        self.gamma = AgentConfig.GAMMA
        self.epsilon = AgentConfig.EPSILON

        self.model = DQN(state_dim, action_dim)

        # Target network:
        self.target_model = copy.deepcopy(self.model)
        self.target_model.eval()

        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=AgentConfig.LR
        )

        self.criterion = nn.SmoothL1Loss()

        self.replay_buffer = ReplayBuffer(ReplayBufferConfig.BUFFER_SIZE)

        self.batch_size = ReplayBufferConfig.BATCH_SIZE

        self.target_update = 1000
        self.train_steps = 0

        self.action_dim = action_dim
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        
        state = torch.FloatTensor(state).unsqueeze(0)

        with torch.no_grad():
            q_values = self.model(state)

        return torch.argmax(q_values).item()
    
    def train(self):

        if len(self.replay_buffer) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = \
            self.replay_buffer.sample(self.batch_size)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        current_q = self.model(states).gather(1, actions).squeeze(1)

        with torch.no_grad():
            next_q = self.target_model(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)

        loss = self.criterion(current_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.train_steps += 1

        if self.train_steps % self.target_update == 0:
            self.target_model.load_state_dict(self.model.state_dict())