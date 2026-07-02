import numpy as np

class ReplayBuffer:
    def __init__(self, capacity, state_shape):
        self.capacity = capacity
        self.ptr = 0  # Points to the current empty slot
        self.size = 0 # Tracks how full the buffer is
        
        self.states = np.zeros((capacity, *state_shape), dtype=np.uint8)
        self.next_states = np.zeros((capacity, *state_shape), dtype=np.uint8)
        self.actions = np.zeros((capacity,), dtype=np.int64)
        self.rewards = np.zeros((capacity,), dtype=np.float32)
        self.dones = np.zeros((capacity,), dtype=np.float32)

    def add(self, state, action, reward, next_state, done):
        # Overwrite the oldest data at the current pointer
        self.states[self.ptr] = state
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.next_states[self.ptr] = next_state
        self.dones[self.ptr] = done

        # Move the pointer, loop back to 0 if we hit the capacity
        self.ptr = (self.ptr + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def force_memorize(self, state, action, reward, next_state, done, duplicates=5):
        for _ in range(duplicates):
            self.add(state, action, reward, next_state, done)

    def sample(self, batch_size):
        idxs = np.random.randint(0, self.size, size=batch_size)

        return (
            self.states[idxs],
            self.actions[idxs],
            self.rewards[idxs],
            self.next_states[idxs],
            self.dones[idxs]
        )

    def __len__(self):
        return self.size