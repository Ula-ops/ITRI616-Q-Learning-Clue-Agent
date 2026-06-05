"""Interactive training mode where a real player guesses the AI's clues."""

import json
import os
import random

from cards import get_clues_for_round
from game_environment import GameEnvironment, ROUND_NAMES
from q_learning_agent import QLearningAgent


SAVE_FILE = "interactive_learning.json"


def normalize_answer(text):
    """Normalize guesses so small typing differences matter less."""
    return "".join(character.lower() for character in text if character.isalnum())


def load_agent(environment):
    """Create an agent and load previous interactive learning if it exists."""
    agent = QLearningAgent(actions=environment.get_actions(), epsilon=0.35, min_epsilon=0.05)

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            agent.load_data(json.load(file))

    return agent


def save_agent(agent):
    """Save the agent's learned clue values."""
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(agent.to_data(), file, indent=2)


def get_round_instruction(round_number):
    """Explain what kind of clue is allowed in this round."""
    if round_number == 1:
        return "Words allowed: full sentence clue."
    if round_number == 2:
        return "Words allowed: one word only."
    return "Words allowed: none. Use actions only."


def play_interactive_game(rounds=3, cards_per_game=10):
    """Let a real player guess clues and train the AI from the answers."""
    environment = GameEnvironment(seed=42)
    agent = load_agent(environment)
    randomizer = random.Random()
    game_cards = environment.cards.copy()
    randomizer.shuffle(game_cards)
    game_cards = game_cards[:cards_per_game]

    print("Interactive 30 Seconds-style AI trainer")
    print("=" * 44)
    print("The AI chooses an actual clue. You type your guess.")
    print("Type 'quit' to stop.\n")
    print("This game will use the same 10 cards in all three rounds.")

    correct_guesses = 0
    attempts = 0

    for round_number in range(1, rounds + 1):
        round_name = ROUND_NAMES[round_number]
        cards = game_cards.copy()
        randomizer.shuffle(cards)

        print(f"\nRound {round_number}: {round_name}")
        print(get_round_instruction(round_number))
        print("-" * 44)

        for card in cards:
            state = (card, round_number)
            allowed_actions = get_clues_for_round(card, round_number)
            clue = agent.choose_action(
                state, training=True, allowed_actions=allowed_actions
            )

            print()
            if round_number == 3:
                print(f"Action: {clue}")
            else:
                print(f"Clue: {clue}")

            guess = input("Your guess: ").strip()

            if guess.lower() == "quit":
                save_agent(agent)
                print("\nProgress saved.")
                return

            success = normalize_answer(guess) == normalize_answer(card)
            reward = 1.0 if success else -0.25
            agent.update(state=state, action=clue, reward=reward)
            agent.decay_epsilon()

            attempts += 1
            if success:
                correct_guesses += 1
                print("Correct.")
            else:
                print(f"Not correct. The answer was: {card}")

    save_agent(agent)

    success_rate = correct_guesses / attempts if attempts else 0.0
    print("\nGame finished.")
    print(f"Correct guesses: {correct_guesses}/{attempts}")
    print(f"Success rate: {success_rate:.2%}")
    print(f"Learning saved in: {SAVE_FILE}")
