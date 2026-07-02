# Pokémon Red: Deep Q-Learning Agent
**Course:** Introduction to Machine Learning  

## Project Overview
The goal of this project is to develop a Reinforcement Learning (RL) agent capable of navigating and playing the 1996 Game Boy classic, *Pokémon Red*. The project implements a Deep Q-Network (DQN) to teach the agent RL fundamentals, focusing on state-based learning, reward shaping, and memory management.

While fully solving a partial-observable RPG is beyond the scope of a baseline DQN, this project serves as a deep dive into the practical challenges of applied RL, including reward hacking, exploration vs. exploitation trade-offs, and catastrophic forgetting.

---

## Tech Stack & Architecture
* **Language:** Python
* **Machine Learning Framework:** PyTorch (DQN implementation)
* **Environment:** PyBoy (Game Boy Emulator) wrapped with Gymnasium
* **Logging:** TensorBoard (Tracking loss, epsilon decay, and episodic rewards)

---

## Methodology

### 1. State Representation
Instead of relying strictly on pixel-delta (screen changes) which introduces noise, this agent utilizes RAM-based state extraction for deterministic learning. The neural network receives:
* Current Map ID, X/Y Coordinates.
* Game event flags (e.g., Oak Cutscene triggered, Pokémon count).
* **Frame Stacking:** The environment stacks the last 4 frames to give the agent a sense of momentum and short-term memory, mitigating partial observability.

### 2. Action Space & Macro-Actions
To address the Game Boy's context-sensitive movement (where pressing a direction might only *turn* the character rather than take a step), the action space is restricted to standard inputs `[UP, DOWN, LEFT, RIGHT, A, B]` and wrapped in a **24-frame Macro-Action**. This forces the emulator to complete full walking animations, preventing the agent from getting stuck turning in place.

### 3. The Reward Function
The reward configuration balances exploration with critical game milestones:
* **Exploration:** `+1.0` for discovering new tiles/maps.
* **Milestones:** `+150` for reaching Professor Oak, `+200` for obtaining a starter Pokémon.
* **Penalties:** Scaled penalties for revisiting tiles, getting stuck, or oscillating between maps to discourage loitering.

---

## Challenges & Findings

Throughout training, the agent discovered several fascinating RL exploits that required targeted algorithmic patches:

* **Reward Hacking (The Lab Exploit):** Early iterations of the agent realized it could walk through the front door of Oak's lab (a low-effort path) to trigger the same reward as navigating the tall grass. This was patched using Y-coordinate and map-transition verification.
* **The "Safe Harbor" Effect (Local Maxima):** When faced with loop penalties for exploring, the agent mathematically deduced that spinning in place or walking directly into walls yielded fewer negative points than exploring. This required implementing a "Boredom Timer" to forcefully terminate episodes lacking progress.
* **Catastrophic Forgetting:** As the agent successfully reached the Rival battle (scoring ~1000+ points), the rarity of this event caused the network to overwrite the winning policy with "failure" data from early exploration. 

---

## Future Work
While the current agent successfully learned to navigate to the lab and obtain a Pokémon under high exploration (ε), stabilizing the policy during exploitation remains an ongoing challenge. Future improvements would include:
1. Implementing true Prioritized Experience Replay (PER).
2. Transitioning from DQN to Proximal Policy Optimization (PPO) for better continuous policy updates.
3. Adding Recurrent Neural Networks (RNN/LSTM) to replace simple frame stacking.