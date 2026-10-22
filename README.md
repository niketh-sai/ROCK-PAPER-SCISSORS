# 🎮 Rock Paper Scissors - Ultimate Gaming Arena

A premium, feature-rich Rock Paper Scissors gaming application built with Python and Streamlit. Features adaptive AI opponents, multiplayer support, advanced analytics, and a stunning futuristic gaming interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🎯 Game Modes
- **Player vs Computer**: Compete against an adaptive AI opponent
- **Player vs Player**: Two players on the same device
- **Best of Series**: Best of 3, 5, 7, or unlimited rounds

### 🤖 AI Difficulty Levels
- **Easy**: Completely random moves, no strategy
- **Medium**: Mix of random and strategic moves based on move frequency
- **Hard**: Adaptive AI with pattern recognition and predictive counter-strategies

### 📊 Advanced Statistics
- Real-time scoreboard with wins, losses, and draws
- Winning streak tracking (current and best)
- Move frequency analysis
- Win rate calculation
- Interactive charts using Plotly
- Detailed match history

### 🎨 Premium UI/UX
- Futuristic gaming interface with glassmorphism design
- Deep navy and black background with neon accents
- Smooth animations and transitions
- Responsive design for desktop and mobile
- Countdown animation before reveal
- Sound effects (toggleable)

### 🏆 Series Mode
- Best of 3, 5, 7, or unlimited rounds
- Series score tracking
- Automatic series winner announcement

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository** (or download the files):
```bash
cd ROCK-PAPER-SCISSORS
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
rock_paper_scissors/
│
├── app.py                  # Main Streamlit application
├── game_logic.py           # Core game rules and logic
├── ai_engine.py            # AI opponent implementation
├── statistics.py          # Statistics and analytics
├── styles.css              # Custom CSS styling
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
└── assets/
    ├── images/            # Image assets (if needed)
    ├── icons/             # Icon assets (if needed)
    └── sounds/            # Sound effects (placeholder)
```

## 🎮 How to Play

### Player vs Computer
1. Select your difficulty level (Easy, Medium, or Hard)
2. Click on Rock, Paper, or Scissors
3. Watch the countdown animation
4. See the result and updated statistics
5. Play again to improve your stats

### Player vs Player
1. Player 1 selects their move (hidden from view)
2. Player 2 selects their move
3. Both moves are revealed simultaneously
4. Winner is announced and statistics updated

### Best of Series
1. Select series length (3, 5, 7, or unlimited)
2. Play rounds against the computer
3. First to reach the majority wins the series
4. Series statistics are tracked separately

## 🤖 AI Strategies Explained

### Easy Mode
- **Strategy**: Completely random selection
- **Learning**: No pattern recognition or learning
- **Win Rate**: Approximately 33% (statistical average)

### Medium Mode
- **Strategy**: 60% random, 40% strategic
- **Learning**: Tracks move frequency and occasionally counters the most frequent move
- **Adaptation**: Adjusts to player's most common move
- **Win Rate**: Approximately 40-45%

### Hard Mode
- **Strategy**: Adaptive with pattern recognition
- **Learning**:
  - Tracks last 50 player moves
  - Analyzes move patterns (n-gram analysis)
  - Predicts next move based on historical patterns
  - Counters predicted moves with 70% probability
  - Counters most frequent move with 80% probability
- **Adaptation**: Continuously learns from player behavior
- **Randomness**: Controlled randomness to avoid being exploited
- **Win Rate**: Approximately 50-55% (depending on player predictability)

**Note**: The Hard AI does not claim to perfectly predict random human behavior. It uses statistical analysis and pattern recognition to make educated predictions, which can be effective against players with predictable patterns.

## 📊 Statistics Dashboard

The statistics dashboard provides comprehensive analytics:

### Overview
- Total games played
- Overall win rate
- Best winning streak
- Most frequently used move

### Move Distribution
- Pie chart showing percentage of each move used
- Helps identify player tendencies

### Win/Loss Distribution
- Bar chart comparing wins, losses, and draws
- Visual representation of performance

### Detailed History
- Complete match history with timestamps
- Filterable and sortable
- Shows moves, results, and difficulty level

## 🎨 Design Features

### Visual Theme
- **Background**: Deep navy (#0a0e27) to black (#050714) gradient
- **Accents**: Electric blue, purple gradients, neon cyan
- **Cards**: Glassmorphism with blur effects
- **Typography**: Modern gaming fonts with proper hierarchy

### Animations
- Glow effects on hover
- Smooth transitions between states
- Countdown animation (3 → 2 → 1 → SHOOT!)
- Result reveal animation
- Selection card animations

### Responsive Design
- Optimized for desktop, tablet, and mobile
- Flexible grid layouts
- Touch-friendly interface
- Adaptive card sizes

### Customization
- **Colors**: Modify CSS variables in `styles.css`
- **Difficulty**: Adjust AI parameters in `ai_engine.py`
- **Statistics**: Extend `statistics.py` for additional metrics

## 📝 Technical Details

### Technologies Used
- **Python 3.11+**: Core language
- **Streamlit**: Web application framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations
- **HTML5/CSS3**: Custom styling
- **JavaScript**: Interactive elements

### Architecture
- **Modular Design**: Separate modules for game logic, AI, and statistics
- **Session State**: Streamlit session state for persistent data
- **State Management**: Centralized state for game progress
- **Event-Driven**: Button clicks trigger state updates

### Performance
- Optimized for smooth animations
- Efficient state management
- Minimal reruns
- Responsive rendering



## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add actual sound effects
- Implement user accounts with database
- Add more game modes
- Improve AI algorithms
- Add multiplayer over network
- Create leaderboards

## 📄 License

This project is open source and available under the MIT License.

