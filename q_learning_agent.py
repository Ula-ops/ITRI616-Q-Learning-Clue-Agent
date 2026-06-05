"""Q-learning agent for choosing clues.

Q-learning stores a value, called a Q-value, for each state-action pair. In
this project a state is (card, round_number), and an action is an actual clue.
Higher Q-values mean the agent has learned that a clue usually performs well
for that card and round.
"""

import random


class QLearningAgent:
    """Beginner-friendly Q-learning agent."""

    def __init__(
        self,
        actions,
        learning_rate=0.15,
        discount_factor=0.0,
        epsilon=1.0,
        epsilon_decay=0.995,
        min_epsilon=0.05,
        seed=7,
    ):
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.random = random.Random(seed)

        # The Q-table is a dictionary:
        # {
        #     (card, round_number): {
        #         "clue_text": q_value
        #     }
        # }
        self.q_table = {}

    def _ensure_state_exists(self, state):
        """Add a new state to the Q-table if the agent has not seen it yet."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}

    def choose_action(self, state, training=True, allowed_actions=None):
        """Choose a clue using exploration or exploitation.

        Exploration means trying a random clue to learn more.
        Exploitation means choosing the clue with the highest known Q-value.
        """
        self._ensure_state_exists(state)
        actions = allowed_actions if allowed_actions is not None else self.actions

        if training and self.random.random() < self.epsilon:
            return self.random.choice(actions)

        return self.best_action(state, allowed_actions=actions)

    def best_action(self, state, allowed_actions=None):
        """Return the action with the highest Q-value for a state."""
        self._ensure_state_exists(state)
        action_values = self.q_table[state]
        actions = allowed_actions if allowed_actions is not None else self.actions
        return max(actions, key=lambda action: action_values[action])

    def update(self, state, action, reward, next_state=None):
        """Update one Q-value using the Q-learning formula.

        Formula:
            new_q = old_q + learning_rate * (target - old_q)

        Since each card attempt is a short one-step decision, this project uses
        discount_factor = 0.0 by default. That means the agent focuses on the
        immediate reward from the chosen clue.
        """
        self._ensure_state_exists(state)

        old_q = self.q_table[state][action]

        if next_state is None:
            future_reward = 0.0
        else:
            self._ensure_state_exists(next_state)
            future_reward = max(self.q_table[next_state].values())

        target = reward + self.discount_factor * future_reward
        new_q = old_q + self.learning_rate * (target - old_q)
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        """Slowly reduce exploration as the agent gains experience."""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def to_data(self):
        """Convert learned values to JSON-friendly data."""
        rows = []

        for (card, round_number), action_values in self.q_table.items():
            rows.append(
                {
                    "card": card,
                    "round_number": round_number,
                    "action_values": action_values,
                }
            )

        return {
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "epsilon": self.epsilon,
            "epsilon_decay": self.epsilon_decay,
            "min_epsilon": self.min_epsilon,
            "q_table": rows,
        }

    def load_data(self, data):
        """Load previously learned values from JSON-friendly data."""
        self.learning_rate = data.get("learning_rate", self.learning_rate)
        self.discount_factor = data.get("discount_factor", self.discount_factor)
        self.epsilon = data.get("epsilon", self.epsilon)
        self.epsilon_decay = data.get("epsilon_decay", self.epsilon_decay)
        self.min_epsilon = data.get("min_epsilon", self.min_epsilon)

        self.q_table = {}
        for row in data.get("q_table", []):
            state = (row["card"], row["round_number"])
            self.q_table[state] = {
                action: float(value)
                for action, value in row["action_values"].items()
                if action in self.actions
            }
            for action in self.actions:
                self.q_table[state].setdefault(action, 0.0)
