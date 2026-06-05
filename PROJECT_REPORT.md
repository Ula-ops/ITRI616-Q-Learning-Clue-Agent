# Q-Learning Clue-Giving Agent for a Southern African Card Guessing Game

## 1. Introduction

This project designs and implements an intelligent game-playing agent for a local Southern African clue-based card guessing game. The game is inspired by social card guessing games in which a clue giver helps a team guess as many cards as possible within a limited time. The implemented version uses South African-themed cards, such as `Robben Island`, `Gautrain`, `Rooibos tea`, `Bunny chow`, and `District Six`.

The aim of the project is to formulate the game as a well-posed learning problem using the Task, Experience, and Performance (TEP) structure. The intelligent agent acts as the clue giver. For every card and round, it must choose the clue that is most likely to help the team guess the correct card. The project demonstrates that the agent's performance improves as it gains experience through repeated simulated games.

The current implementation uses Q-learning. The agent does not generate completely new language. Instead, each card has a fixed set of possible clues. The agent learns which actual clue works best for each card and round.

## 2. Game Description

The game uses 20 South African-themed cards. Each complete game has 3 rounds. The same cards are used in each round, but the clue rules become more restrictive:

- Round 1: full sentence clues are allowed.
- Round 2: only one-word clues are allowed.
- Round 3: only action clues are allowed.

Each card has three possible clues for each round. Therefore, a card has:

- 3 sentence clues for round 1,
- 3 one-word clues for round 2,
- 3 action clues for round 3.

The game is turn-based. A turn represents one team's 30-second opportunity to guess cards. In the simulation, each card attempt takes a random amount of time between 4 and 8 seconds. This means that only a limited number of clue-and-guess attempts can fit into one turn. If a card is guessed correctly, it is removed from the current round's pile. If it is guessed incorrectly, it remains available and can be attempted again later.

## 3. Formal TEP Definition

### Task

The task is to choose the best clue for a given card in a given round.

Formally:

```text
State = (card, round_number)
Action = one valid clue for that card and round
```

The agent's objective is to select the clue that maximises the chance that the team correctly guesses the card.

### Experience

The agent gains experience by repeatedly playing simulated games. During training, the agent tries clues, receives feedback, and updates its Q-values. A successful clue receives a positive reward, while an unsuccessful clue receives a small negative reward.

The project also includes an interactive mode in which a human player can guess the AI's clues. In that mode, the agent learns from real user feedback. However, the experimental results in this report are based on the simulated training experiment so that performance can be measured consistently.

### Performance

Performance is measured using several values:

- Average score: the number of cards successfully guessed per 30-second turn.
- Average reward: the total reward earned in a simulated game.
- Success rate: the percentage of card attempts that are guessed correctly.
- Average turns: the number of 30-second turns needed to finish the full game.
- Average attempts: the number of clue-and-guess attempts made during testing.

The main requirement is to show that performance improves with experience. This is shown by comparing the agent's early training performance with its final training performance and by plotting the learning curves in `training_results.png`.

## 4. Learning Algorithm

The learning algorithm used is Q-learning. Q-learning is suitable for this project because the agent must learn the value of choosing different actions in different states. In this project, each action is an actual clue.

The Q-table stores values in this form:

```text
Q[(card, round_number)][clue] = learned value
```

A higher Q-value means that the agent has learned that a clue is more useful for a particular card and round.

The update rule used by the agent is:

```text
new_q = old_q + learning_rate * (target - old_q)
target = reward + discount_factor * future_reward
```

In this implementation, the discount factor is set to `0.0`. This is because each clue attempt is treated as a short one-step decision. The result of the current clue is what matters most, rather than a long future sequence of decisions.

The agent uses epsilon-greedy action selection:

- Exploration: the agent sometimes chooses a random clue to learn more.
- Exploitation: the agent chooses the clue with the highest known Q-value.

At the start of training, epsilon is high, so the agent explores more. After each training game, epsilon decays. This means the agent gradually shifts from exploration to exploitation as it gains experience.

## 5. Implementation Overview

The project is implemented in Python.

The main files are:

- `cards.py`: stores the 20 cards and the clue options for each round.
- `game_environment.py`: simulates the game world, turn timing, clue success, rewards, scoring, and game progression.
- `q_learning_agent.py`: implements the Q-learning agent and Q-table.
- `experiment.py`: trains the agent, evaluates it, prints results, and creates the graph.
- `interactive_game.py`: allows a human player to play and train the agent manually.
- `main.py`: provides the menu for choosing interactive mode or simulated training.

The environment contains hidden success probabilities for clues. For each card and round, the first clue has the highest success probability, the second clue has a medium probability, and the third clue has a lower probability. The agent does not know these probabilities. It must discover better clues through trial and error.

Later rounds receive a small probability increase because players have already seen the cards. This models the memory effect that occurs in repeated-round clue games.

## 6. Experimental Setup

The main experiment trains the agent for 1000 simulated games. After training, the agent is tested with exploration switched off. This means the trained agent uses the best clue it has learned instead of choosing random exploratory clues.

The experiment records:

- score per training episode,
- reward per training episode,
- success rate per training episode,
- number of turns per training episode.

The graph uses a 50-game moving average to smooth the learning curves. The graph has two panels:

- the top panel shows average score over time,
- the bottom panel shows average reward over time.

The two metrics are shown separately because they use different scales. Score is measured as cards per turn, while reward is measured as total game reward.

## 7. Experimental Results

The latest simulated experiment used the following setup:

```text
Training episodes: 1000
Cards per game: 20
Rounds per game: 3
Teams: Team A and Team B
Turn length: 30 seconds
Claimed cards per completed game: 60
```

The training results were:

```text
Starting average score: 2.70 cards per turn
Final average score:    3.52 cards per turn
Improvement:            30.61%

Starting average reward: 56.27
Final average reward:    58.63
Starting success rate:   62.17%
Final success rate:      81.71%
Starting average turns:  22.46
Final average turns:     17.12
```

The trained agent was then tested with exploration switched off:

```text
Average score:        3.51 cards per turn
Average reward:       58.66
Average success rate: 81.96%
Average turns:        17.19
Average attempts:     73.42
```

These results show that the agent improved with experience. The success rate increased from 62.17% to 81.71%, and the average number of turns needed to finish the game decreased from 22.46 to 17.12. The average score also increased from 2.70 to 3.52 cards per turn.

The cards-per-turn value may appear low, but this is due to the 30-second turn limit. Each card attempt takes between 4 and 8 simulated seconds, so only a few attempts can fit into one turn. Therefore, an average of about 3.5 correct cards per turn is reasonable in the context of the simulation.

## 8. Critical Analysis

The project successfully demonstrates the main requirement: performance improves with experience. Q-learning is appropriate because the agent repeatedly chooses from a fixed set of possible clues and receives feedback after each choice.

The strongest evidence of learning is the improvement in success rate. The agent moved from 62.17% success early in training to 81.71% success near the end of training. This shows that the agent learned to prefer better clues over weaker clues.

The decrease in average turns is also important. Because every full game eventually claims all 60 card-round combinations, a better agent does not necessarily claim more total cards. Instead, it claims them more efficiently. Finishing the full game in fewer turns shows that the agent is helping the team guess cards more quickly.

However, the project also has limitations. The simulation uses manually designed hidden success probabilities. This means the simulated players do not behave like real humans. A real player's understanding of a clue may depend on language, culture, prior knowledge, spelling, and personal associations. The current simulation simplifies this by assigning fixed probabilities.

Another limitation is that the agent chooses from pre-written clues. It does not create original clues using natural language generation. This keeps the project focused and easier to evaluate, but it limits the agent's creativity.

The reward function is also simple. A correct guess gives a positive reward, and an incorrect guess gives a small negative reward. This is enough to demonstrate learning, but a more advanced version could reward faster guesses, penalise repeated failures more strongly, or adjust rewards based on round difficulty.

Despite these limitations, the project is well aligned with the assignment. It defines a clear local game, formulates the agent's role as a learning problem, implements a learning algorithm, collects experimental data, and demonstrates measurable improvement.

## 9. Reflection

This project showed how an everyday social game can be transformed into a formal machine learning problem. The most important design step was defining the agent's task clearly. At first, the agent could have been described as choosing a general clue strategy, but the final version is more meaningful because the agent chooses the actual clue used in the game.

The TEP framework helped structure the project. The task, experience, and performance definitions made it easier to decide what the agent should learn, how it should learn, and how improvement should be measured.

The project also showed the difference between building a game and building a learning agent. The game rules alone are not enough for the assignment. The important part is that the agent receives experience and improves its performance over time.

The main challenge was designing a simulation that was simple enough to implement but still realistic enough to support learning. The final simulation is not a perfect model of human guessing, but it is suitable for demonstrating Q-learning and performance improvement.

Future improvements could include collecting real human guessing data, increasing the number of cards, adding more clue options, using more detailed reward functions, or allowing the agent to generate new clues with a language model.

## 10. Conclusion

The project implements a Q-learning clue-giving agent for a Southern African card guessing game. The game is formulated as a well-posed learning problem using the TEP structure. The agent learns from repeated simulated games by updating Q-values for clue choices.

The experimental results show clear improvement with experience. The agent's success rate increased from 62.17% to 81.71%, and its average score increased from 2.70 to 3.52 cards per turn. This demonstrates that the agent learned to choose better clues over time.

Overall, the project satisfies the goal of designing and implementing an intelligent game agent whose performance improves through experience.
