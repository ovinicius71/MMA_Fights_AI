# UFC AI Fight Simulator

This repository contains an MMA/UFC fight simulator where AI agents make strategic decisions based on fighter attributes, probabilistic models, and stochastic game search algorithms.

---

## 🚀 Overview

The **UFC AI Fight Simulator** allows simulating bouts between agents programmed with different strategies, ranging from simple rule-based approaches to advanced search and reinforcement learning algorithms. Virtual fighters have attribute profiles (strength, accuracy, stamina, etc.) and choose strikes and defenses based on probability distributions, MDP/POMDP policies, Expectimax, and MCTS.

---

## 🎯 Key Features

- Fighter modeling with real attributes and performance history.
- Discrete-event simulation environment (rounds and time-steps) with stochastic events.
- Action selection via:
  - Heuristic rule-based agents (sense–think–act).
  - Expectimax with chance nodes (stochastic games).
  - Monte Carlo Tree Search (MCTS).
- Integration of ML models:
  - Classification/regression to predict strike success rates (Scikit-Learn).
  - Reinforcement Learning (Q-Learning or DQN) to optimize policies through self-play.
- Collection and analysis of metrics: win rate, average damage, number of rounds.
- Automated tournaments between different agents for strategy comparison.

---

## 📚 Topics Covered

1. **Agents and Environments** (2.1, 2.4)
2. **Markov Decision Processes (MDP/POMDP)**
3. **Stochastic Modeling** (Monte Carlo, probability distributions)
4. **Search Algorithms for Stochastic Games**
   - Expectimax & α–β adapted
   - Monte Carlo Tree Search (MCTS)
5. **Data Engineering**
   - Data collection, cleaning, and feature engineering (pandas, MMA stats APIs)
6. **Machine Learning**
   - Logistic regression, decision trees (Scikit-Learn)
   - Q-Learning / DQN (TensorFlow or PyTorch)
7. **Discrete-Event Simulation** (SimPy or custom engine)
8. **Software Architecture**
   - Sense–Think–Act pattern
   - Modular and configurable design
9. **Evaluation and Metrics**
   - A/B experiments
   - Performance statistics and visualizations (matplotlib)

---

## 🛠 Technologies Used

- **Language:** Python 3.8+
- **Data & ML:** pandas, numpy, scikit-learn, TensorFlow / PyTorch
- **Simulation:** SimPy (or custom engine)
- **Search & Games:** networkx (graph structures), custom MCTS implementation
- **Analysis & Visualization:** matplotlib
- **Testing:** pytest
- **Version Control:** Git

---

## 🏗 Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ufc-ai-simulator.git
   cd ufc-ai-simulator
