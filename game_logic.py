"""
Game Logic Module for Rock Paper Scissors
Handles core game rules, move validation, and winner determination.
"""

from enum import Enum
from typing import Optional, Tuple
import random


class Move(Enum):
    """Enumeration of possible moves in Rock Paper Scissors."""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    def __str__(self):
        return self.value.capitalize()

    @classmethod
    def from_string(cls, move_str: str) -> Optional['Move']:
        """Convert string to Move enum."""
        try:
            return cls(move_str.lower())
        except ValueError:
            return None

    @property
    def emoji(self) -> str:
        """Return emoji representation of the move."""
        emojis = {
            Move.ROCK: "🪨",
            Move.PAPER: "📄",
            Move.SCISSORS: "✂️"
        }
        return emojis[self]


class Result(Enum):
    """Enumeration of possible game results."""
    PLAYER_WIN = "player_win"
    COMPUTER_WIN = "computer_win"
    DRAW = "draw"
    PLAYER1_WIN = "player1_win"
    PLAYER2_WIN = "player2_win"

    def __str__(self):
        display_names = {
            Result.PLAYER_WIN: "YOU WIN!",
            Result.COMPUTER_WIN: "COMPUTER WINS!",
            Result.DRAW: "IT'S A DRAW!",
            Result.PLAYER1_WIN: "PLAYER 1 WINS!",
            Result.PLAYER2_WIN: "PLAYER 2 WINS!"
        }
        return display_names[self]


def determine_winner(player_move: Move, computer_move: Move) -> Result:
    """
    Determine the winner of a round based on moves.

    Rules:
    - Rock defeats Scissors
    - Scissors defeats Paper
    - Paper defeats Rock
    - Identical selections result in a draw

    Args:
        player_move: The player's move
        computer_move: The computer's move

    Returns:
        Result enum indicating the winner
    """
    if player_move == computer_move:
        return Result.DRAW

    # Rock beats Scissors
    if player_move == Move.ROCK and computer_move == Move.SCISSORS:
        return Result.PLAYER_WIN
    if computer_move == Move.ROCK and player_move == Move.SCISSORS:
        return Result.COMPUTER_WIN

    # Scissors beats Paper
    if player_move == Move.SCISSORS and computer_move == Move.PAPER:
        return Result.PLAYER_WIN
    if computer_move == Move.SCISSORS and player_move == Move.PAPER:
        return Result.COMPUTER_WIN

    # Paper beats Rock
    if player_move == Move.PAPER and computer_move == Move.ROCK:
        return Result.PLAYER_WIN
    if computer_move == Move.PAPER and player_move == Move.ROCK:
        return Result.COMPUTER_WIN

    # Should never reach here, but default to draw
    return Result.DRAW


def determine_winner_pvp(player1_move: Move, player2_move: Move) -> Result:
    """
    Determine the winner in Player vs Player mode.

    Args:
        player1_move: Player 1's move
        player2_move: Player 2's move

    Returns:
        Result enum indicating the winner
    """
    if player1_move == player2_move:
        return Result.DRAW

    # Rock beats Scissors
    if player1_move == Move.ROCK and player2_move == Move.SCISSORS:
        return Result.PLAYER1_WIN
    if player2_move == Move.ROCK and player1_move == Move.SCISSORS:
        return Result.PLAYER2_WIN

    # Scissors beats Paper
    if player1_move == Move.SCISSORS and player2_move == Move.PAPER:
        return Result.PLAYER1_WIN
    if player2_move == Move.SCISSORS and player1_move == Move.PAPER:
        return Result.PLAYER2_WIN

    # Paper beats Rock
    if player1_move == Move.PAPER and player2_move == Move.ROCK:
        return Result.PLAYER1_WIN
    if player2_move == Move.PAPER and player1_move == Move.ROCK:
        return Result.PLAYER2_WIN

    return Result.DRAW


def get_random_move() -> Move:
    """Return a random move."""
    return random.choice(list(Move))


def get_counter_move(move: Move) -> Move:
    """
    Return the move that counters the given move.

    Args:
        move: The move to counter

    Returns:
        The move that defeats the given move
    """
    counters = {
        Move.ROCK: Move.PAPER,
        Move.PAPER: Move.SCISSORS,
        Move.SCISSORS: Move.ROCK
    }
    return counters[move]


def validate_move(move_str: str) -> bool:
    """
    Validate if a string is a valid move.

    Args:
        move_str: String to validate

    Returns:
        True if valid, False otherwise
    """
    return Move.from_string(move_str) is not None


def get_all_moves() -> list[Move]:
    """Return list of all possible moves."""
    return list(Move)
