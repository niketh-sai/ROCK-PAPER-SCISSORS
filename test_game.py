"""
Test script to verify game logic and AI engine functionality.
"""

from game_logic import Move, Result, determine_winner, determine_winner_pvp
from ai_engine import AIEngine, Difficulty
from statistics import GameStatistics

def test_game_rules():
    """Test all game rules."""
    print("Testing Game Rules...")
    assert determine_winner(Move.ROCK, Move.SCISSORS) == Result.PLAYER_WIN
    assert determine_winner(Move.SCISSORS, Move.PAPER) == Result.PLAYER_WIN
    assert determine_winner(Move.PAPER, Move.ROCK) == Result.PLAYER_WIN
    assert determine_winner(Move.SCISSORS, Move.ROCK) == Result.COMPUTER_WIN
    assert determine_winner(Move.PAPER, Move.SCISSORS) == Result.COMPUTER_WIN
    assert determine_winner(Move.ROCK, Move.PAPER) == Result.COMPUTER_WIN
    assert determine_winner(Move.ROCK, Move.ROCK) == Result.DRAW
    assert determine_winner(Move.PAPER, Move.PAPER) == Result.DRAW
    assert determine_winner(Move.SCISSORS, Move.SCISSORS) == Result.DRAW
    print("[PASS] All game rules passed!")

def test_ai_engine():
    """Test AI engine with different difficulties."""
    print("\nTesting AI Engine...")

    # Test Easy AI
    easy_ai = AIEngine(Difficulty.EASY)
    moves = [easy_ai.get_move() for _ in range(10)]
    assert len(moves) == 10
    assert all(move in [Move.ROCK, Move.PAPER, Move.SCISSORS] for move in moves)
    print("[PASS] Easy AI works!")

    # Test Medium AI
    medium_ai = AIEngine(Difficulty.MEDIUM)
    for _ in range(5):
        medium_ai.record_player_move(Move.ROCK)
    move = medium_ai.get_move()
    assert move in [Move.ROCK, Move.PAPER, Move.SCISSORS]
    print("[PASS] Medium AI works!")

    # Test Hard AI
    hard_ai = AIEngine(Difficulty.HARD)
    for _ in range(10):
        hard_ai.record_player_move(Move.ROCK)
    move = hard_ai.get_move()
    assert move in [Move.ROCK, Move.PAPER, Move.SCISSORS]
    print("[PASS] Hard AI works!")

def test_statistics():
    """Test statistics tracking."""
    print("\nTesting Statistics...")
    stats = GameStatistics()

    stats.record_match(Move.ROCK, Move.SCISSORS, Result.PLAYER_WIN, "medium")
    assert stats.player_wins == 1
    assert stats.total_rounds == 1
    assert stats.current_streak == 1
    assert stats.highest_streak == 1

    stats.record_match(Move.PAPER, Move.SCISSORS, Result.COMPUTER_WIN, "medium")
    assert stats.computer_wins == 1
    assert stats.current_streak == 0

    stats.record_match(Move.ROCK, Move.ROCK, Result.DRAW, "medium")
    assert stats.draws == 1

    summary = stats.get_summary()
    assert summary['total_rounds'] == 3
    assert summary['player_wins'] == 1
    assert summary['computer_wins'] == 1
    assert summary['draws'] == 1
    print("[PASS] Statistics tracking works!")

def test_pvp():
    """Test Player vs Player mode."""
    print("\nTesting PvP Mode...")
    result = determine_winner_pvp(Move.ROCK, Move.SCISSORS)
    assert result == Result.PLAYER1_WIN

    result = determine_winner_pvp(Move.SCISSORS, Move.ROCK)
    assert result == Result.PLAYER2_WIN

    result = determine_winner_pvp(Move.ROCK, Move.ROCK)
    assert result == Result.DRAW
    print("[PASS] PvP mode works!")

if __name__ == "__main__":
    print("=" * 50)
    print("Running Rock Paper Scissors Tests")
    print("=" * 50)

    try:
        test_game_rules()
        test_ai_engine()
        test_statistics()
        test_pvp()

        print("\n" + "=" * 50)
        print("[PASS] ALL TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        raise
