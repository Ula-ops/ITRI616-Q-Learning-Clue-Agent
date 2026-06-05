"""Main file for running the AI mini-project."""

from experiment import run_experiment
from interactive_game import play_interactive_game


if __name__ == "__main__":
    print("AI mini-project")
    print("1. Play interactive training game")
    print("2. Run simulated training experiment")

    choice = input("Choose 1 or 2, then press Enter: ").strip()

    if choice == "2":
        run_experiment(episodes=1000)
    else:
        play_interactive_game()
