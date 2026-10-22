"""
AI Engine Module for Rock Paper Scissors
Implements adaptive AI opponents with varying difficulty levels.
"""

from enum import Enum
from typing import Optional, Dict, List
import random
from collections import Counter, deque
from game_logic import Move, get_random_move, get_counter_move


class Difficulty(Enum):
    """Enumeration of AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def __str__(self):
        return self.value.capitalize()


class AIEngine:
    """
    Adaptive AI opponent that learns from player behavior.
    Implements three difficulty levels with different strategies.
    """

    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM):
        """
        Initialize the AI engine.

        Args:
            difficulty: The difficulty level of the AI
        """
        self.difficulty = difficulty
        self.move_history: deque = deque(maxlen=50)  # Track last 50 moves
        self.pattern_history: deque = deque(maxlen=20)  # Track move patterns
        self.move_counter: Counter = Counter()  # Count move frequency
        self.total_moves: int = 0

    def set_difficulty(self, difficulty: Difficulty):
        """Change the AI difficulty level."""
        self.difficulty = difficulty

    def record_player_move(self, move: Move):
        """
        Record a player's move for pattern analysis.

        Args:
            move: The player's move
        """
        self.move_history.append(move)
        self.move_counter[move] += 1
        self.total_moves += 1

        # Record patterns (sequence of last 2 moves)
        if len(self.move_history) >= 2:
            pattern = (self.move_history[-2], self.move_history[-1])
            self.pattern_history.append(pattern)

    def _get_most_frequent_move(self) -> Optional[Move]:
        """Get the player's most frequently used move."""
        if not self.move_counter:
            return None
        return self.move_counter.most_common(1)[0][0]

    def _predict_next_move(self) -> Optional[Move]:
        """
        Predict the player's next move based on pattern analysis.
        Uses n-gram analysis on move sequences.
        """
        if len(self.move_history) < 3:
            return None

        # Look for patterns in the last 2 moves
        last_two = (self.move_history[-2], self.move_history[-1])

        # Find what usually follows this pattern
        possible_next_moves = []
        for i in range(len(self.pattern_history) - 1):
            if self.pattern_history[i] == last_two:
                next_pattern = self.pattern_history[i + 1]
                possible_next_moves.append(next_pattern[1])

        if not possible_next_moves:
            return None

        # Return the most likely next move
        counter = Counter(possible_next_moves)
        return counter.most_common(1)[0][0]

    def _get_easy_move(self) -> Move:
        """
        Easy AI: Completely random moves.
        No strategy or pattern recognition.
        """
        return get_random_move()

    def _get_medium_move(self) -> Move:
        """
        Medium AI: Mix of random and strategic moves.
        Tracks move frequency and occasionally counters it.
        """
        # 60% random, 40% strategic
        if random.random() < 0.6:
            return get_random_move()

        # Try to counter the most frequent move
        most_frequent = self._get_most_frequent_move()
        if most_frequent:
            return get_counter_move(most_frequent)

        return get_random_move()

    def _get_hard_move(self) -> Move:
        """
        Hard AI: Adaptive strategy with pattern recognition.
        Uses move history, frequency analysis, and pattern prediction.
        """
        if self.total_moves < 5:
            # Not enough data, use random moves initially
            return get_random_move()

        # Try to predict the next move
        predicted_move = self._predict_next_move()

        if predicted_move:
            # Counter the predicted move with 70% probability
            if random.random() < 0.7:
                return get_counter_move(predicted_move)

        # Fall back to countering the most frequent move
        most_frequent = self._get_most_frequent_move()
        if most_frequent:
            # Counter with 80% probability to avoid being too predictable
            if random.random() < 0.8:
                return get_counter_move(most_frequent)

        # Add some randomness to avoid being exploited
        return get_random_move()

    def get_move(self) -> Move:
        """
        Get the AI's move based on current difficulty.

        Returns:
            The AI's selected move
        """
        if self.difficulty == Difficulty.EASY:
            return self._get_easy_move()
        elif self.difficulty == Difficulty.MEDIUM:
            return self._get_medium_move()
        else:  # HARD
            return self._get_hard_move()

    def reset(self):
        """Reset the AI's learning data."""
        self.move_history.clear()
        self.pattern_history.clear()
        self.move_counter.clear()
        self.total_moves = 0

    def get_statistics(self) -> Dict:
        """
        Get AI learning statistics.

        Returns:
            Dictionary containing AI statistics
        """
        return {
            "difficulty": str(self.difficulty),
            "total_moves_tracked": self.total_moves,
            "move_frequency": {
                str(move): count
                for move, count in self.move_counter.items()
            },
            "pattern_count": len(self.pattern_history)
        }


class AIFactory:
    """Factory class for creating AI instances."""

    @staticmethod
    def create_ai(difficulty: str = "medium") -> AIEngine:
        """
        Create an AI engine with the specified difficulty.

        Args:
            difficulty: String representation of difficulty level

        Returns:
            AIEngine instance
        """
        try:
            diff = Difficulty(difficulty.lower())
        except ValueError:
            diff = Difficulty.MEDIUM

        return AIEngine(diff)
