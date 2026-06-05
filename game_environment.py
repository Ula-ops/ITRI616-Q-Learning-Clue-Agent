"""Simulated 30 Seconds-style game environment.

This file represents the "world" that the Q-learning agent interacts with.
It simulates whether a chosen clue would probably work for a specific card in a
specific round.
"""

import random

from cards import get_all_clues, get_cards, get_clues_for_round


ROUND_NAMES = {
    1: "Normal clue-giving",
    2: "One-word clues",
    3: "Gesture/action clues",
}


TEAMS = ["Team A", "Team B"]
TURN_SECONDS = 30


class GameEnvironment:
    """A small reinforcement learning environment for the card game.

    Task:
        The agent chooses an actual clue for each (card, round) state.

    Experience:
        The same 20 cards appear in all 3 rounds, and many simulated games are
        played during training. The agent repeatedly receives feedback for the
        same card and round combinations.

    Performance:
        The environment returns rewards and scores so that improvement can be
        measured over time.
    """

    def __init__(self, seed=42):
        self.cards = get_cards()
        self.rounds = [1, 2, 3]
        self.clues = get_all_clues()
        self.teams = TEAMS
        self.turn_seconds = TURN_SECONDS
        self.random = random.Random(seed)
        self.success_probabilities = self._build_success_probability_table()

    def _build_success_probability_table(self):
        """Create the hidden probabilities used by the simulation.

        The Q-learning agent does not receive this table. It must discover good
        clues by trying actions and learning from rewards.
        """
        table = {}

        for card in self.cards:
            for round_number in self.rounds:
                state = (card, round_number)
                table[state] = {}
                allowed_clues = get_clues_for_round(card, round_number)

                for clue_index, clue in enumerate(allowed_clues):
                    if clue_index == 0:
                        probability = 0.78
                    elif clue_index == 1:
                        probability = 0.55
                    else:
                        probability = 0.35

                    # Later rounds are easier because players have already
                    # seen the cards. This models the memory effect.
                    probability += 0.04 * (round_number - 1)

                    table[state][clue] = min(probability, 0.95)

        return table

    def get_actions(self):
        """Return all possible clue actions."""
        return self.clues.copy()

    def get_allowed_actions(self, state):
        """Return only the clues allowed for the state's round."""
        card, round_number = state
        return get_clues_for_round(card, round_number)

    def get_states(self):
        """Return every (card, round) state in the game."""
        return [(card, round_number) for round_number in self.rounds for card in self.cards]

    def attempt_card(self, card, round_number, clue):
        """Simulate one card attempt and return reward information.

        A successful guess gives +1 reward and +1 score. A failed guess gives a
        small negative reward so that the agent learns to avoid weak clues.
        """
        state = (card, round_number)
        success_probability = self.success_probabilities[state][clue]
        success = self.random.random() < success_probability

        reward = 1.0 if success else -0.10
        score = 1 if success else 0

        return {
            "success": success,
            "reward": reward,
            "score": score,
            "success_probability": success_probability,
        }

    def _simulate_attempts_allowed_in_turn(self):
        """Estimate how many cards fit into a 30-second turn.

        Real 30 Seconds turns are time-limited, not card-limited. For a simple
        simulation, each attempted card takes a random number of seconds. The
        loop counts how many attempts can happen before 30 seconds runs out.
        """
        seconds_used = 0
        attempts_allowed = 0

        while True:
            seconds_for_next_card = self.random.randint(4, 8)

            if seconds_used + seconds_for_next_card > self.turn_seconds:
                break

            seconds_used += seconds_for_next_card
            attempts_allowed += 1

        # This protects the simulation from an unlikely zero-attempt turn.
        return max(1, attempts_allowed)

    def play_game(self, agent, training=True):
        """Play one full 3-round game with the supplied agent.

        The same 20 cards are reused in each round. Within a round, teams take
        alternating 30-second turns until all 20 cards have been guessed and
        claimed. Correct cards are removed from that round's pile. Failed cards
        stay available and can be attempted again on a later turn.
        """
        total_claimed_cards = 0
        total_reward = 0.0
        correct_guesses = 0
        attempts = 0
        turns = 0
        team_scores = {team: 0 for team in self.teams}
        round_scores = {}

        for round_number in self.rounds:
            available_cards = self.cards.copy()
            self.random.shuffle(available_cards)
            current_team_index = 0
            round_scores[round_number] = {team: 0 for team in self.teams}

            while available_cards:
                current_team = self.teams[current_team_index]
                attempts_allowed = self._simulate_attempts_allowed_in_turn()
                turns += 1

                for _ in range(attempts_allowed):
                    if not available_cards:
                        break

                    # The card is drawn from the remaining round pile. If it is
                    # guessed correctly, that team claims it. If not, it stays
                    # in the pile for a later turn.
                    card = self.random.choice(available_cards)
                    state = (card, round_number)
                    allowed_actions = self.get_allowed_actions(state)
                    clue = agent.choose_action(
                        state, training=training, allowed_actions=allowed_actions
                    )
                    result = self.attempt_card(card, round_number, clue)

                    if training:
                        agent.update(
                            state=state,
                            action=clue,
                            reward=result["reward"],
                            next_state=None,
                        )

                    total_reward += result["reward"]
                    attempts += 1

                    if result["success"]:
                        available_cards.remove(card)
                        total_claimed_cards += 1
                        correct_guesses += 1
                        team_scores[current_team] += 1
                        round_scores[round_number][current_team] += 1

                # After one 30-second turn, play passes to the other team.
                current_team_index = (current_team_index + 1) % len(self.teams)

        failed_attempts = attempts - correct_guesses
        success_rate = correct_guesses / attempts if attempts else 0.0
        cards_claimed_per_turn = total_claimed_cards / turns if turns else 0.0

        return {
            # "score" is an efficiency score because all 60 cards are always
            # eventually claimed once every round is completed.
            "score": cards_claimed_per_turn,
            "reward": total_reward,
            "correct_guesses": correct_guesses,
            "claimed_cards": total_claimed_cards,
            "failed_attempts": failed_attempts,
            "attempts": attempts,
            "turns": turns,
            "success_rate": success_rate,
            "team_scores": team_scores,
            "round_scores": round_scores,
        }
