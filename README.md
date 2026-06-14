# Langton's Ant RL Simulation

A dual-mode Python simulation built with **Pygame** that explores emergent complexity. The project showcases the transition of a classic **Langton's Ant cellular automaton** into a self-optimizing **Reinforcement Learning (RL)** environment using a model-free Q-learning agent.

---

## 📌 Project Overview

This repository contains two distinct simulation paradigms running on a 2D toroidal (wrapping) grid:
1. **The Classic Simulation:** A deterministic cellular automaton driven by strict, simple localized rules that unexpectedly yield complex macro-level emergent behaviors (the famous "highway").
2. **The Q-Learning Agent:** An artificial intelligence extension where the hardcoded movement rules are completely replaced by an $\epsilon$-greedy Q-learning algorithm, letting the agent discover its own optimal navigation policy based on tile-color states and a reward framework.

---

##  The Original Langton's Ant

In the traditional simulation, multiple ants navigate the grid based on simple binary rules:
* On a **white tile**, turn $90^\circ$ right, flip the tile color to black, and move forward.
* On a **black tile**, turn $90^\circ$ left, flip the tile color to white, and move forward.

### Emergent Phenomena & The "Highway"
Despite the simplicity of these rules, the simulation progresses through three distinct phases:
1. **Simplicity:** In the first few hundred steps, it creates simple, symmetric patterns.
2. **Chaos:** For thousands of steps, the ant displays pseudo-random, chaotic behavior, painting a disorganized patch of black and white tiles.
3. **Emergence (The Highway):** Eventually, the ant falls into a repetitive 104-step cycle that builds a diagonal, stratified path—a "highway"—indefinitely. Because the environment is configured as a toroidal grid, the ant wraps around the screen, collides with its past chaotic trail, breaks its loop, and triggers an ongoing cycle of chaos and highway reconstruction.

---

##  The Reinforcement Learning Extension

The extension translates the cellular automaton into a strict **Markov Decision Process (MDP)** by stripping away the deterministic rules and introducing a `QLearningAgent`.

### Mathematical Framework
* **State Space ($S$):** Binary representation based on the color of the current tile ($S \in \{0: \text{White}, 1: \text{Black}\}$).
* **Action Space ($A$):** 4 discrete movement directions ($A \in \{0: \text{Right}, 1: \text{Down}, 2: \text{Left}, 3: \text{Up}\}$).
* **Policy Exploration:** Controlled via an **Epsilon-Greedy ($\epsilon$-greedy)** strategy ($\epsilon = 0.1$) to balance exploratory random actions and the exploitation of known high-value paths.

### Reward Design
To incentivize continuous exploration and mapping, the agent operates under the following reward function:
* **$+1.0$ Reward:** Awarded for moving onto a white tile and flipping it black (incentivizing active landscape modification).
* **$-0.1$ Penalty:** Incurred for stepping onto an already black tile (discouraging localized looping and stagnant behavior).

### Policy Convergence & Emergent "Barcodes"
When left to optimize over thousands of steps, the agent's Q-table converges to highly specialized values:

```text
Final Converged Q-Table Readout:
State 0 (White): [Right: 9.85,  Down: 9.35,  Left: 7.82,  Up: 9.49] -> Prefers RIGHT
State 1 (Black): [Right: 5.49,  Down: 7.73,  Left: 5.44,  Up: 6.61] -> Prefers DOWN

