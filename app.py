"""
Rock Paper Scissors - Premium Gaming Arena
A sophisticated, minimalist gaming application with adaptive AI and professional UI.
"""

import streamlit as st
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from game_logic import Move, Result, determine_winner, determine_winner_pvp, get_all_moves
from ai_engine import AIEngine, Difficulty, AIFactory
from statistics import GameStatistics

# Page Configuration
st.set_page_config(
    page_title="RPS Arena",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# SVG Icons
SVG_ROCK = """
<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M32 8C18.7 8 8 18.7 8 32s10.7 24 24 24 24-10.7 24-24S45.3 8 32 8zm0 4c11 0 20 9 20 20s-9 20-20 20-20-9-20-20 9-20 20-20z" fill="#FF7043"/>
    <path d="M24 24h16v4H24v-4zm0 8h16v4H24v-4zm0 8h16v4H24v-4z" fill="#FF7043"/>
</svg>
"""

SVG_PAPER = """
<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 12h24v40H20V12zm4 4v32h16V16H24z" fill="#FF7043"/>
    <path d="M24 20h16v2H24v-2zm0 6h16v2H24v-2zm0 6h16v2H24v-2zm0 6h16v2H24v-2z" fill="#FF7043"/>
</svg>
"""

SVG_SCISSORS = """
<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M28 12l-8 20-8-20v-4h16v4zm0 4l8 20 8-20v-4H28v4z" fill="#FF7043"/>
    <circle cx="20" cy="36" r="4" fill="#FF7043"/>
    <circle cx="44" cy="36" r="4" fill="#FF7043"/>
</svg>
"""

SVG_GAMEPAD = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4-3c-.83 0-1.5-.67-1.5-1.5S18.67 9 19.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" fill="#FF7043"/>
</svg>
"""

SVG_USERS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="#FF7043"/>
</svg>
"""

SVG_TROPHY = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z" fill="#FF7043"/>
</svg>
"""

SVG_STATS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="#FF7043"/>
</svg>
"""

SVG_SETTINGS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="#FF7043"/>
</svg>
"""

SVG_HISTORY = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" fill="#FF7043"/>
</svg>
"""

SVG_HOME = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="#FF7043"/>
</svg>
"""

# Initialize Session State
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "pvc"
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "medium"
    if "series_length" not in st.session_state:
        st.session_state.series_length = 3
    if "sound_enabled" not in st.session_state:
        st.session_state.sound_enabled = False
    if "ai_engine" not in st.session_state:
        st.session_state.ai_engine = AIFactory.create_ai("medium")
    if "statistics" not in st.session_state:
        st.session_state.statistics = GameStatistics()
    if "player1_move" not in st.session_state:
        st.session_state.player1_move = None
    if "player2_move" not in st.session_state:
        st.session_state.player2_move = None
    if "round_result" not in st.session_state:
        st.session_state.round_result = None
    if "countdown_active" not in st.session_state:
        st.session_state.countdown_active = False
    if "show_result" not in st.session_state:
        st.session_state.show_result = False

init_session_state()

# Sound Effects
def play_sound(sound_type):
    if st.session_state.sound_enabled:
        pass

# Render Header
def render_header():
    st.markdown("""
    <div class="header">
        <div class="header-left">
            <div class="header-logo">RPS</div>
            <div class="header-brand">ARENA</div>
        </div>
        <div class="header-right">
            <button class="header-nav-btn" onclick="location.reload()">Statistics</button>
            <button class="header-nav-btn" onclick="location.reload()">History</button>
            <button class="header-nav-btn" onclick="location.reload()">Settings</button>
            <button class="header-nav-btn" onclick="location.reload()">Menu</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Landing Page
def render_landing_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<h1 class="section-heading">Select Game Mode</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="mode-card active">
            <div class="mode-card-icon">{SVG_GAMEPAD}</div>
            <div class="mode-card-title">Player vs Computer</div>
            <div class="mode-card-desc">Challenge our adaptive AI</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play", key="mode_pvc", use_container_width=True):
            st.session_state.game_mode = "pvc"
            st.session_state.page = "game"
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="mode-card">
            <div class="mode-card-icon">{SVG_USERS}</div>
            <div class="mode-card-title">Player vs Player</div>
            <div class="mode-card-desc">Local multiplayer</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play", key="mode_pvp", use_container_width=True):
            st.session_state.game_mode = "pvp"
            st.session_state.page = "game"
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="mode-card">
            <div class="mode-card-icon">{SVG_TROPHY}</div>
            <div class="mode-card-title">Best of Series</div>
            <div class="mode-card-desc">Competitive series mode</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play", key="mode_series", use_container_width=True):
            st.session_state.game_mode = "series"
            st.session_state.page = "game"
            st.rerun()

    st.markdown('<h2 class="section-heading" style="margin-top: 48px;">Difficulty</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Easy", key="diff_easy", use_container_width=True):
            st.session_state.difficulty = "easy"
            st.session_state.ai_engine = AIFactory.create_ai("easy")
    with col2:
        if st.button("Medium", key="diff_medium", use_container_width=True):
            st.session_state.difficulty = "medium"
            st.session_state.ai_engine = AIFactory.create_ai("medium")
    with col3:
        if st.button("Hard", key="diff_hard", use_container_width=True):
            st.session_state.difficulty = "hard"
            st.session_state.ai_engine = AIFactory.create_ai("hard")

    st.markdown(f'<p class="text-center" style="color: var(--text-secondary); margin-top: 16px;">Current: {st.session_state.difficulty.upper()}</p>', unsafe_allow_html=True)

    # Quick Stats
    stats = st.session_state.statistics.get_summary()
    st.markdown('<h2 class="section-heading" style="margin-top: 48px;">Your Statistics</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{stats['total_rounds']}</div>
            <div class="score-label">Games</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="score-card wins">
            <div class="score-value">{stats['player_wins']}</div>
            <div class="score-label">Wins</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="score-card losses">
            <div class="score-value">{stats['computer_wins']}</div>
            <div class="score-label">Losses</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{stats['win_percentage']}%</div>
            <div class="score-label">Win Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Game Page
def render_game_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Menu", key="game_back"):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        if st.button("Statistics", key="game_stats"):
            st.session_state.page = "statistics"
            st.rerun()

    # Game Mode Indicator
    mode_names = {"pvc": "Player vs Computer", "pvp": "Player vs Player", "series": "Best of Series"}
    st.markdown(f'<p class="text-center" style="color: var(--accent-primary); font-weight: 600; margin: 24px 0;">{mode_names[st.session_state.game_mode]}</p>', unsafe_allow_html=True)

    # Render game mode
    if st.session_state.game_mode == "pvc":
        render_pvc_game()
    elif st.session_state.game_mode == "pvp":
        render_pvp_game()
    elif st.session_state.game_mode == "series":
        render_series_game()

    # Scoreboard
    render_scoreboard()

    # History
    render_match_history()

    st.markdown('</div>', unsafe_allow_html=True)

# Player vs Computer
def render_pvc_game():
    if st.session_state.countdown_active:
        render_countdown()
    elif st.session_state.show_result:
        render_result()
    else:
        render_selection_cards()

# Player vs Player
def render_pvp_game():
    if st.session_state.player1_move is None:
        st.markdown('<h2 class="section-heading text-center">Player 1 - Select Your Move</h2>', unsafe_allow_html=True)
        render_selection_cards(player=1)
    elif st.session_state.player2_move is None:
        st.markdown('<h2 class="section-heading text-center">Player 2 - Select Your Move</h2>', unsafe_allow_html=True)
        render_selection_cards(player=2)
    else:
        render_pvp_result()

# Best of Series
def render_series_game():
    series_score = st.session_state.statistics.get_series_score(st.session_state.series_length)

    if st.session_state.series_length != 999:
        wins_needed = (st.session_state.series_length // 2) + 1
        if series_score['player'] >= wins_needed:
            st.markdown('<div class="result-panel"><div class="result-text win">You Win the Series!</div></div>', unsafe_allow_html=True)
            if st.button("New Series", key="new_series", use_container_width=True):
                st.session_state.statistics.reset()
                st.session_state.ai_engine.reset()
                st.session_state.show_result = False
                st.rerun()
            return
        elif series_score['computer'] >= wins_needed:
            st.markdown('<div class="result-panel"><div class="result-text lose">Computer Wins the Series</div></div>', unsafe_allow_html=True)
            if st.button("New Series", key="new_series2", use_container_width=True):
                st.session_state.statistics.reset()
                st.session_state.ai_engine.reset()
                st.session_state.show_result = False
                st.rerun()
            return

    if st.session_state.countdown_active:
        render_countdown()
    elif st.session_state.show_result:
        render_result()
    else:
        render_selection_cards()

# Selection Cards
def render_selection_cards(player=None):
    st.markdown('<h2 class="section-heading text-center">Choose Your Move</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="move-card-icon text-center">{SVG_ROCK}</div>', unsafe_allow_html=True)
        if st.button("Rock", key="btn_rock", use_container_width=True):
            handle_move_selection(Move.ROCK, player)

    with col2:
        st.markdown(f'<div class="move-card-icon text-center">{SVG_PAPER}</div>', unsafe_allow_html=True)
        if st.button("Paper", key="btn_paper", use_container_width=True):
            handle_move_selection(Move.PAPER, player)

    with col3:
        st.markdown(f'<div class="move-card-icon text-center">{SVG_SCISSORS}</div>', unsafe_allow_html=True)
        if st.button("Scissors", key="btn_scissors", use_container_width=True):
            handle_move_selection(Move.SCISSORS, player)

def handle_move_selection(move, player=None):
    play_sound("selection")

    if st.session_state.game_mode == "pvc":
        st.session_state.ai_engine.record_player_move(move)
        ai_move = st.session_state.ai_engine.get_move()
        st.session_state.player_move = move
        st.session_state.computer_move = ai_move
        st.session_state.countdown_active = True
        st.rerun()

    elif st.session_state.game_mode == "pvp":
        if player == 1:
            st.session_state.player1_move = move
        elif player == 2:
            st.session_state.player2_move = move
        st.rerun()

    elif st.session_state.game_mode == "series":
        st.session_state.ai_engine.record_player_move(move)
        ai_move = st.session_state.ai_engine.get_move()
        st.session_state.player_move = move
        st.session_state.computer_move = ai_move
        st.session_state.countdown_active = True
        st.rerun()

# Countdown
def render_countdown():
    st.markdown('<div class="countdown-display">3</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="countdown-display">2</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="countdown-display">1</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="countdown-display">SHOOT!</div>', unsafe_allow_html=True)
    time.sleep(0.5)

    st.session_state.countdown_active = False
    st.session_state.show_result = True
    st.rerun()

# Result Display
def render_result():
    player_move = st.session_state.player_move
    computer_move = st.session_state.computer_move
    result = determine_winner(player_move, computer_move)

    st.session_state.statistics.record_match(
        player_move, computer_move, result, st.session_state.difficulty
    )

    if result == Result.PLAYER_WIN:
        play_sound("victory")
        result_class = "win"
        result_text = "You Win!"
    elif result == Result.COMPUTER_WIN:
        play_sound("defeat")
        result_class = "lose"
        result_text = "Computer Wins"
    else:
        play_sound("draw")
        result_class = "draw"
        result_text = "It's a Draw"

    st.markdown(f"""
    <div class="game-arena">
        <div class="arena-card">
            <div class="arena-card-name">You</div>
            <div class="arena-card-icon">{get_move_svg(player_move)}</div>
            <div class="arena-card-status">{player_move.value.capitalize()}</div>
        </div>
        <div class="arena-vs">VS</div>
        <div class="arena-card">
            <div class="arena-card-name">Computer</div>
            <div class="arena-card-icon">{get_move_svg(computer_move)}</div>
            <div class="arena-card-status">{computer_move.value.capitalize()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="result-panel"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

    if st.button("Play Again", key="play_again", use_container_width=True):
        st.session_state.show_result = False
        st.session_state.player_move = None
        st.session_state.computer_move = None
        st.rerun()

# PvP Result
def render_pvp_result():
    player1_move = st.session_state.player1_move
    player2_move = st.session_state.player2_move
    result = determine_winner_pvp(player1_move, player2_move)

    st.session_state.statistics.record_match(
        player1_move, player2_move, result, None
    )

    if result == Result.PLAYER1_WIN:
        result_class = "win"
        result_text = "Player 1 Wins!"
    elif result == Result.PLAYER2_WIN:
        result_class = "lose"
        result_text = "Player 2 Wins!"
    else:
        result_class = "draw"
        result_text = "It's a Draw"

    st.markdown(f"""
    <div class="game-arena">
        <div class="arena-card">
            <div class="arena-card-name">Player 1</div>
            <div class="arena-card-icon">{get_move_svg(player1_move)}</div>
            <div class="arena-card-status">{player1_move.value.capitalize()}</div>
        </div>
        <div class="arena-vs">VS</div>
        <div class="arena-card">
            <div class="arena-card-name">Player 2</div>
            <div class="arena-card-icon">{get_move_svg(player2_move)}</div>
            <div class="arena-card-status">{player2_move.value.capitalize()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="result-panel"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

    if st.button("Play Again", key="pvp_play_again", use_container_width=True):
        st.session_state.player1_move = None
        st.session_state.player2_move = None
        st.rerun()

def get_move_svg(move):
    if move == Move.ROCK:
        return SVG_ROCK
    elif move == Move.PAPER:
        return SVG_PAPER
    else:
        return SVG_SCISSORS

# Scoreboard
def render_scoreboard():
    stats = st.session_state.statistics.get_summary()

    st.markdown('<h2 class="section-heading">Scoreboard</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="score-card wins">
            <div class="score-value">{stats['player_wins']}</div>
            <div class="score-label">Wins</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="score-card losses">
            <div class="score-value">{stats['computer_wins']}</div>
            <div class="score-label">Losses</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="score-card draws">
            <div class="score-value">{stats['draws']}</div>
            <div class="score-label">Draws</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{stats['total_rounds']}</div>
            <div class="score-label">Total</div>
        </div>
        """, unsafe_allow_html=True)

# Match History
def render_match_history():
    st.markdown('<h2 class="section-heading">Recent Matches</h2>', unsafe_allow_html=True)

    recent_matches = st.session_state.statistics.get_recent_matches(10)

    if not recent_matches:
        st.markdown('<p class="text-center" style="color: var(--text-secondary);">No matches played yet.</p>', unsafe_allow_html=True)
        return

    st.markdown('<div class="history-panel">', unsafe_allow_html=True)

    for match in recent_matches:
        if "WIN" in match['result'] and "COMPUTER" not in match['result']:
            result_class = "win"
        elif "LOSE" in match['result'] or "COMPUTER" in match['result']:
            result_class = "lose"
        else:
            result_class = "draw"

        st.markdown(f"""
        <div class="history-item">
            <div class="history-info">Round {match['round']}: {match['player_move']} vs {match['opponent_move']}</div>
            <div class="history-result {result_class}">{match['result']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Statistics Page
def render_statistics_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<h1 class="section-heading">Statistics</h1>', unsafe_allow_html=True)

    stats = st.session_state.statistics.get_summary()

    # Overview
    st.markdown('<h2 class="section-heading">Overview</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['total_rounds']}</div>
            <div class="stat-label">Total Games</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['win_percentage']}%</div>
            <div class="stat-label">Win Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['highest_streak']}</div>
            <div class="stat-label">Best Streak</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['most_frequent_move'] or 'N/A'}</div>
            <div class="stat-label">Most Used</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    st.markdown('<h2 class="section-heading" style="margin-top: 48px;">Move Distribution</h2>', unsafe_allow_html=True)

    move_percentages = stats['move_percentages']
    if sum(move_percentages.values()) > 0:
        fig = px.pie(
            values=list(move_percentages.values()),
            names=list(move_percentages.keys()),
            title="Move Usage",
            color_discrete_sequence=['#FF7043', '#4CAF80', '#FFB74D']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            title_font_color='#FFFFFF'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<p class="text-center" style="color: var(--text-secondary);">No data available yet.</p>', unsafe_allow_html=True)

    # History Table
    st.markdown('<h2 class="section-heading" style="margin-top: 48px;">Detailed History</h2>', unsafe_allow_html=True)

    df = st.session_state.statistics.get_history_dataframe()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.markdown('<p class="text-center" style="color: var(--text-secondary);">No matches played yet.</p>', unsafe_allow_html=True)

    # Reset
    if st.button("Reset Statistics", key="reset_stats", use_container_width=True):
        st.session_state.statistics.reset()
        st.session_state.ai_engine.reset()
        st.rerun()

    if st.button("Back to Menu", key="stats_back", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown('<h2 style="color: white; margin-bottom: 24px;">Settings</h2>', unsafe_allow_html=True)

        st.session_state.sound_enabled = st.checkbox("Sound Effects", value=st.session_state.sound_enabled)

        st.markdown('<h3 style="color: white; margin-top: 24px;">Difficulty</h3>', unsafe_allow_html=True)
        difficulty = st.selectbox(
            "AI Difficulty",
            ["Easy", "Medium", "Hard"],
            index=["easy", "medium", "hard"].index(st.session_state.difficulty)
        )
        if difficulty.lower() != st.session_state.difficulty:
            st.session_state.difficulty = difficulty.lower()
            st.session_state.ai_engine = AIFactory.create_ai(difficulty.lower())
            st.rerun()

        st.markdown('<h3 style="color: white; margin-top: 24px;">AI Learning</h3>', unsafe_allow_html=True)
        ai_stats = st.session_state.ai_engine.get_statistics()
        st.markdown(f"""
        <div style='color: var(--text-secondary); font-size: 13px;'>
        <p>Difficulty: {ai_stats['difficulty']}</p>
        <p>Moves Tracked: {ai_stats['total_moves_tracked']}</p>
        <p>Patterns Found: {ai_stats['pattern_count']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<h3 style="color: white; margin-top: 24px;">Quick Actions</h3>', unsafe_allow_html=True)

        if st.button("Back to Landing", key="sidebar_landing", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

        if st.button("New Game", key="sidebar_new_game", use_container_width=True):
            st.session_state.page = "game"
            st.session_state.show_result = False
            st.session_state.player_move = None
            st.session_state.computer_move = None
            st.session_state.player1_move = None
            st.session_state.player2_move = None
            st.rerun()

        if st.button("Statistics", key="sidebar_stats", use_container_width=True):
            st.session_state.page = "statistics"
            st.rerun()

        if st.button("Reset All", key="sidebar_reset", use_container_width=True):
            st.session_state.statistics.reset()
            st.session_state.ai_engine.reset()
            st.session_state.show_result = False
            st.session_state.player_move = None
            st.session_state.computer_move = None
            st.session_state.player1_move = None
            st.session_state.player2_move = None
            st.rerun()

# Main App
def main():
    render_sidebar()

    if st.session_state.page == "landing":
        render_landing_page()
    elif st.session_state.page == "game":
        render_game_page()
    elif st.session_state.page == "statistics":
        render_statistics_page()

if __name__ == "__main__":
    main()
