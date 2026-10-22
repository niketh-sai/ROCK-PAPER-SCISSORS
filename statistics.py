"""
Statistics Module for Rock Paper Scissors
Handles game statistics, match history, and analytics.
"""

from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter
import pandas as pd
from game_logic import Move, Result


class MatchRecord:
    """Represents a single match record."""

    def __init__(
        self,
        round_number: int,
        player_move: Move,
        opponent_move: Move,
        result: Result,
        difficulty: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.round_number = round_number
        self.player_move = player_move
        self.opponent_move = opponent_move
        self.result = result
        self.difficulty = difficulty
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """Convert match record to dictionary."""
        return {
            "round": self.round_number,
            "player_move": str(self.player_move),
            "opponent_move": str(self.opponent_move),
            "result": str(self.result),
            "difficulty": self.difficulty,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }


class GameStatistics:
    """
    Manages game statistics and match history.
    Tracks wins, losses, draws, streaks, and move patterns.
    """

    def __init__(self):
        """Initialize game statistics."""
        self.player_wins: int = 0
        self.computer_wins: int = 0
        self.draws: int = 0
        self.total_rounds: int = 0
        self.current_streak: int = 0
        self.highest_streak: int = 0
        self.match_history: List[MatchRecord] = []
        self.move_history: List[Move] = []
        self.player1_wins: int = 0  # For PvP mode
        self.player2_wins: int = 0  # For PvP mode

    def record_match(
        self,
        player_move: Move,
        opponent_move: Move,
        result: Result,
        difficulty: Optional[str] = None
    ):
        """
        Record a match result.

        Args:
            player_move: The player's move
            opponent_move: The opponent's move
            result: The match result
            difficulty: The AI difficulty level (if applicable)
        """
        self.total_rounds += 1
        self.move_history.append(player_move)

        match_record = MatchRecord(
            round_number=self.total_rounds,
            player_move=player_move,
            opponent_move=opponent_move,
            result=result,
            difficulty=difficulty
        )
        self.match_history.append(match_record)

        # Update statistics based on result
        if result == Result.PLAYER_WIN:
            self.player_wins += 1
            self.current_streak += 1
            if self.current_streak > self.highest_streak:
                self.highest_streak = self.current_streak
        elif result == Result.COMPUTER_WIN:
            self.computer_wins += 1
            self.current_streak = 0
        elif result == Result.DRAW:
            self.draws += 1
        elif result == Result.PLAYER1_WIN:
            self.player1_wins += 1
        elif result == Result.PLAYER2_WIN:
            self.player2_wins += 1

    def get_win_percentage(self) -> float:
        """Calculate overall win percentage."""
        if self.total_rounds == 0:
            return 0.0
        return (self.player_wins / self.total_rounds) * 100

    def get_move_frequency(self) -> Dict[str, int]:
        """Get frequency of each move."""
        counter = Counter(self.move_history)
        return {str(move): count for move, count in counter.items()}

    def get_move_percentages(self) -> Dict[str, float]:
        """Get percentage of each move used."""
        if not self.move_history:
            return {"Rock": 0.0, "Paper": 0.0, "Scissors": 0.0}

        counter = Counter(self.move_history)
        total = len(self.move_history)
        return {
            str(move): (count / total) * 100
            for move, count in counter.items()
        }

    def get_most_frequent_move(self) -> Optional[str]:
        """Get the most frequently used move."""
        if not self.move_history:
            return None
        counter = Counter(self.move_history)
        return str(counter.most_common(1)[0][0])

    def get_most_successful_move(self) -> Optional[str]:
        """
        Get the move with the highest win rate.
        Returns the move that has won the most times.
        """
        if not self.match_history:
            return None

        move_wins = Counter()
        for match in self.match_history:
            if match.result == Result.PLAYER_WIN:
                move_wins[match.player_move] += 1

        if not move_wins:
            return None

        return str(move_wins.most_common(1)[0][0])

    def get_recent_matches(self, limit: int = 10) -> List[Dict]:
        """
        Get the most recent match records.

        Args:
            limit: Maximum number of matches to return

        Returns:
            List of match dictionaries
        """
        recent = self.match_history[-limit:]
        return [match.to_dict() for match in reversed(recent)]

    def get_summary(self) -> Dict:
        """
        Get a summary of all statistics.

        Returns:
            Dictionary containing all statistics
        """
        return {
            "player_wins": self.player_wins,
            "computer_wins": self.computer_wins,
            "draws": self.draws,
            "total_rounds": self.total_rounds,
            "current_streak": self.current_streak,
            "highest_streak": self.highest_streak,
            "win_percentage": round(self.get_win_percentage(), 2),
            "most_frequent_move": self.get_most_frequent_move(),
            "most_successful_move": self.get_most_successful_move(),
            "move_percentages": self.get_move_percentages()
        }

    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get match history as a pandas DataFrame.

        Returns:
            DataFrame containing match history
        """
        if not self.match_history:
            return pd.DataFrame()

        data = [match.to_dict() for match in self.match_history]
        return pd.DataFrame(data)

    def reset(self):
        """Reset all statistics."""
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.total_rounds = 0
        self.current_streak = 0
        self.highest_streak = 0
        self.match_history.clear()
        self.move_history.clear()
        self.player1_wins = 0
        self.player2_wins = 0

    def get_series_score(self, max_rounds: int) -> Dict[str, int]:
        """
        Get current series score for Best of N mode.

        Args:
            max_rounds: Maximum rounds in the series

        Returns:
            Dictionary with series scores
        """
        return {
            "player": self.player_wins,
            "computer": self.computer_wins,
            "draws": self.draws,
            "rounds_played": self.total_rounds,
            "rounds_remaining": max_rounds - self.total_rounds
        }

    def get_pvp_score(self) -> Dict[str, int]:
        """
        Get current PvP score.

        Returns:
            Dictionary with PvP scores
        """
        return {
            "player1": self.player1_wins,
            "player2": self.player2_wins,
            "draws": self.draws,
            "total_rounds": self.total_rounds
        }
