# Authors: S. El Alaoui and ChatGPT 5.2
# Coins-in-a-line game logic from Homework 1 with additional placeholders for MCTS.
#
# MCTS is written to be:
#  - deterministic-interface: mcts(state, budget, reward_mode, c) -> legal action
#  - safe: never mutates input states (relies on succ creating a fresh State)
#  - simple: random rollouts by default, UCT selection, most-visited final action
#
# Roles:
#  - state.turn is either 'player' or 'ai'
#  - pScore belongs to 'player', aiScore belongs to 'ai'
#  - mcts(...) returns an action for whoever state's turn is (root_player)

from __future__ import annotations

import math
import random
from typing import Dict, Optional, Tuple, List

Action = Tuple[str, int]  # ('L' or 'R', 1 or 2)


class State:
    def __init__(self, coins, pScore: int = 0, aiScore: int = 0, turn: str = "player"):
        self.coins = coins
        self.pScore = pScore
        self.aiScore = aiScore
        self.turn = turn


# ----------------------------
# A1 functions (game + minimax)
# ----------------------------

def player(state: State) -> str:
    """Return whose turn it is: 'player' or 'ai'."""
    return state.turn


def actions(state: State) -> List[Action]:
    """Return legal actions given remaining coins."""
    coins = state.coins
    acts: List[Action] = []
    if len(coins) >= 1:
        acts.append(("L", 1))
        acts.append(("R", 1))
    if len(coins) >= 2:
        acts.append(("L", 2))
        acts.append(("R", 2))
    return acts


def succ(state: State, action: Action) -> State:
    """
    Return successor state after applying action, WITHOUT mutating the input state.
    action = ('L' or 'R', 1 or 2)
    """
    coins = state.coins[:]  # shallow copy is enough for list of ints
    p1, p2 = state.pScore, state.aiScore
    turn = state.turn
    side, count = action

    if action not in actions(state):
        raise ValueError(f"Invalid action {action} for coins={state.coins}")

    if side == "L":
        taken = coins[:count]
        new_coins = coins[count:]
    else:
        taken = coins[-count:]
        new_coins = coins[:-count]

    if turn == "player":
        p1 += sum(taken)
        next_turn = "ai"
    else:
        p2 += sum(taken)
        next_turn = "player"

    return State(new_coins, p1, p2, next_turn)


def terminal(state: State) -> bool:
    """Game ends when no coins remain."""
    return len(state.coins) == 0


def utility(state: State) -> Tuple[int, int]:
    """Return (player_score, ai_score). Only called on terminal states."""
    return state.pScore, state.aiScore


def winner(state: State) -> Optional[str]:
    """
    Return 'player' if player won, 'ai' if ai won, otherwise None.
    (If game in progress, returns None.)
    """
    if not terminal(state):
        return None
    p1, p2 = utility(state)
    if p1 > p2:
        return "player"
    if p2 > p1:
        return "ai"
    return None


def minimax(state: State, is_maximizing: bool):
    """
    Return (best_value, best_action) from perspective of the current recursion role.
    In this file's original convention, we use:
      - is_maximizing=True for AI's decision node
      - terminal value returned as (aiScore - pScore) if maximizing, else opposite
    """
    if terminal(state):
        p1, p2 = utility(state)
        return (p2 - p1 if is_maximizing else p1 - p2), None

    best_val = float("-inf") if is_maximizing else float("inf")
    best_action = None

    for action in actions(state):
        new_state = succ(state, action)
        val, _ = minimax(new_state, not is_maximizing)
        if is_maximizing:
            if val > best_val:
                best_val = val
                best_action = action
        else:
            if val < best_val:
                best_val = val
                best_action = action

    return best_val, best_action


# ----------------------------
# A2: Monte Carlo Tree Search
# ----------------------------


class MCTSNode:
    __slots__ = (
        "state",
        "parent",
        "parent_action",
        "children",
        "untried_actions",
        "N",
        "W",
    )

    def __init__(self, state: State, parent: Optional["MCTSNode"] = None, parent_action: Optional[Action] = None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children: Dict[Action, MCTSNode] = {}
        self.untried_actions: List[Action] = actions(state)[:]  # copy
        self.N = 0              # visit count
        self.W = 0.0            # total reward (from root player's perspective)

def _root_scores(state: State, root_player: str) -> Tuple[int, int]:
    """Return (root_score, opp_score) given a terminal state."""
    if root_player == "player":
        return state.pScore, state.aiScore
    return state.aiScore, state.pScore

def terminal_reward(state, root_player, reward_mode="winloss"):
    """
    Compute terminal reward from the perspective of root_player ('player' or 'ai').

    Returns:
      +1.0 if root_player wins
       0.0 if tie
      -1.0 if root_player loses

    Note: reward_mode is kept for compatibility, but only 'winloss' is supported.
    """
    if winner(state) == root_player:
        return +1.0
    if winner(state) == None:
        return 0.0
    else:    
        return -1.0
        

def uct_score(child, parent_visits, c=math.sqrt(2)):
    """
    UCT score for selection.

    child.W / child.N  +  c * sqrt( ln(parent_visits) / child.N )
    """
    exploitation = (child.W / child.N)
    exploration  = c * math.sqrt(math.log(parent_visits) / child.N)
    ucb = exploitation + exploration
    return ucb


def select_child_uct(node, c=math.sqrt(2)):
    """Return the child node with maximum UCT score."""

    max_child = None
    max_score = float("-inf")
    for child in node.children.values():
        score = uct_score(child, node.N, c)
        if score > max_score:
            max_score = score
            max_child = child
    return max_child
    

def expand(node):
    """
    Expand one untried action from node and return the new child node.
    """
    action = node.untried_actions.pop()       
    child_state = succ(node.state, action)
    child = MCTSNode(child_state, parent=node, parent_action=action)
    node.children[action] = child
    return child


def rollout(state):
    """
    Default rollout policy: play uniformly random legal actions until terminal.
    Must NOT mutate the input state; rely on succ(state, action).
    """
    current = state
    while not terminal(current):
        action = random.choice(actions(current))
        current = succ(current, action)
    return current                               


def backpropagate(node, reward):
    """
    Backpropagate reward up to the root, updating visit counts and total values.
    """
    current = node
    while current is not None:
        current.N += 1
        current.W += reward
        reward   = -reward         
        current  = current.parent


def best_action(root):
    """
    Return the action from root corresponding to the most-visited child (or highest mean value).
    """
    best_action = None
    best_visits = -1
    for action, child in root.children.items():
        if child.N > best_visits:
            best_visits = child.N
            best_action = action

    return best_action


def mcts(state, budget=2000, reward_mode="winloss", c=math.sqrt(2)):
    """
    Run MCTS for 'budget' iterations and return a legal action for the current player.

    - Uses selection / expansion / rollout / backpropagation
    - reward is computed at terminal states via terminal_reward(...)

    Returns: an action in actions(state), or None if state is terminal.
    """
    if terminal(state):
        return None

    root_player = player(state)
    root = MCTSNode(state)

    for _ in range(budget):
        node = root
        while not terminal(node.state) and not node.untried_actions:
            node = select_child_uct(node, c)

        if not terminal(node.state) and node.untried_actions:
            node = expand(node)

        terminal_state = rollout(node.state)

        reward = terminal_reward(terminal_state, root_player, reward_mode)
        backpropagate(node, reward)

    return best_action(root)