"""Training and evaluation experiment for the Q-learning card game agent."""

import os

# Use a non-GUI Matplotlib backend so the project can create a PNG graph on
# lab computers or terminals where Tkinter is not installed correctly.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

import matplotlib.pyplot as plt

from game_environment import GameEnvironment
from q_learning_agent import QLearningAgent


def moving_average(values, window_size):
    """Calculate a simple moving average for smoother graphing."""
    averages = []

    for index in range(len(values)):
        start_index = max(0, index - window_size + 1)
        window = values[start_index : index + 1]
        averages.append(sum(window) / len(window))

    return averages


def train_agent(episodes=1000):
    """Train the Q-learning agent over many simulated games."""
    environment = GameEnvironment(seed=42)
    agent = QLearningAgent(actions=environment.get_actions(), seed=7)

    episode_scores = []
    episode_rewards = []
    episode_success_rates = []
    episode_turns = []

    for episode in range(episodes):
        result = environment.play_game(agent, training=True)

        episode_scores.append(result["score"])
        episode_rewards.append(result["reward"])
        episode_success_rates.append(result["success_rate"])
        episode_turns.append(result["turns"])

        agent.decay_epsilon()

    return environment, agent, episode_scores, episode_rewards, episode_success_rates, episode_turns


def test_agent(environment, agent, games=100):
    """Test the trained agent with exploration switched off."""
    scores = []
    rewards = []
    success_rates = []
    turns = []
    attempts = []

    for _ in range(games):
        result = environment.play_game(agent, training=False)
        scores.append(result["score"])
        rewards.append(result["reward"])
        success_rates.append(result["success_rate"])
        turns.append(result["turns"])
        attempts.append(result["attempts"])

    return {
        "average_score": sum(scores) / len(scores),
        "average_reward": sum(rewards) / len(rewards),
        "average_success_rate": sum(success_rates) / len(success_rates),
        "average_turns": sum(turns) / len(turns),
        "average_attempts": sum(attempts) / len(attempts),
    }


def plot_training_results(scores, rewards, output_file="training_results.png"):
    """Save a graph showing improvement during training."""
    score_average = moving_average(scores, window_size=50)
    reward_average = moving_average(rewards, window_size=50)

    figure, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    figure.suptitle("Q-learning improvement over simulated games")

    axes[0].plot(score_average, color="tab:blue")
    axes[0].set_ylabel("Cards per turn")
    axes[0].set_title("Average score (50-game moving average)")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(reward_average, color="tab:orange")
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Reward")
    axes[1].set_title("Average reward (50-game moving average)")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def print_learned_examples(agent, environment, count=6):
    """Print a few learned policies so the student can explain the result."""
    print("\nExample learned clue choices:")

    shown = 0
    for state in environment.get_states():
        if shown >= count:
            break

        card, round_number = state
        allowed_actions = environment.get_allowed_actions(state)
        best_clue = agent.best_action(state, allowed_actions=allowed_actions)
        print(f"  Card: {card:18s} | Round {round_number} | Clue: {best_clue}")
        shown += 1


def run_experiment(episodes=1000):
    """Run training, testing, graphing, and final reporting."""
    environment, agent, scores, rewards, success_rates, turns = train_agent(
        episodes=episodes
    )

    early_window = scores[:50]
    late_window = scores[-50:]

    starting_average_score = sum(early_window) / len(early_window)
    final_average_score = sum(late_window) / len(late_window)
    improvement_percentage = (
        (final_average_score - starting_average_score) / starting_average_score
    ) * 100

    starting_average_reward = sum(rewards[:50]) / 50
    final_average_reward = sum(rewards[-50:]) / 50
    starting_success_rate = sum(success_rates[:50]) / 50
    final_success_rate = sum(success_rates[-50:]) / 50
    starting_average_turns = sum(turns[:50]) / 50
    final_average_turns = sum(turns[-50:]) / 50

    test_results = test_agent(environment, agent, games=100)
    plot_training_results(scores, rewards)

    print("Q-learning 30 Seconds-style card game experiment")
    print("=" * 52)
    print("TEP structure:")
    print("  Task: choose the best actual clue for each (card, round).")
    print("  Experience: train through repeated simulated games using the same 20 cards.")
    print("  Performance: measure efficiency score, reward, and success rate over time.")
    print()
    print(f"Training episodes: {episodes}")
    print(f"Cards per game: {len(environment.cards)}")
    print(f"Rounds per game: {len(environment.rounds)}")
    print(f"Teams: {', '.join(environment.teams)}")
    print(f"Turn length: {environment.turn_seconds} seconds")
    print(f"Claimed cards per completed game: {len(environment.cards) * len(environment.rounds)}")
    print()
    print(f"Starting average score: {starting_average_score:.2f} cards per turn")
    print(f"Final average score:    {final_average_score:.2f} cards per turn")
    print(f"Improvement:            {improvement_percentage:.2f}%")
    print()
    print(f"Starting average reward: {starting_average_reward:.2f}")
    print(f"Final average reward:    {final_average_reward:.2f}")
    print(f"Starting success rate:    {starting_success_rate:.2%}")
    print(f"Final success rate:       {final_success_rate:.2%}")
    print(f"Starting average turns:   {starting_average_turns:.2f}")
    print(f"Final average turns:      {final_average_turns:.2f}")
    print()
    print("Trained agent test results with exploration switched off:")
    print(f"  Average score:           {test_results['average_score']:.2f} cards per turn")
    print(f"  Average reward:          {test_results['average_reward']:.2f}")
    print(f"  Average success rate:    {test_results['average_success_rate']:.2%}")
    print(f"  Average turns:           {test_results['average_turns']:.2f}")
    print(f"  Average attempts:        {test_results['average_attempts']:.2f}")
    print()
    print("Graph saved as: training_results.png")

    print_learned_examples(agent, environment)

    return {
        "starting_average_score": starting_average_score,
        "final_average_score": final_average_score,
        "improvement_percentage": improvement_percentage,
        "test_results": test_results,
    }
