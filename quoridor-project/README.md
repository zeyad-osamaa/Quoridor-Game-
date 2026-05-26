# Quoridor Game 

---

# Team 
_________Name_______________|______ID_______|
. Omar Ahmed Hassan         | ID: 2300206   |
. Omar Khaled Abdelaty      | ID: 2300366   |
. Omar Ashraf Abdelhamid    | ID: 2301056   |
. Zeyad Osama Mohamed Anwar | ID: 2300678   |

---

# Project description

A fully-featured implementation of the strategy board game **Quoridor**, built with Python and Pygame. Supports Human vs Human and Human vs AI modes with three AI difficulty levels.

> **Demo Video:** (https://drive.google.com/file/d/12zDmey0VNUhdDyxVVCjzBv2UQ1LF1GVC/view?usp=drivesdk)

---

## Table of Contents

- [Game Description](#game-description)
- [Screenshots](#screenshots)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Controls](#controls)
- [Game Modes & AI Difficulty](#game-modes--ai-difficulty)
- [Project Structure](#project-structure)
- [References](#references)

---

## Game Description

Quoridor is a 2-player strategy game played on a 9×9 board. Each player starts with a pawn on the center cell of their baseline and 10 walls.

**Objective:** Be the first to move your pawn to any cell on the opposite baseline.

**On each turn a player must either:**
- Move their pawn one step orthogonally (up, down, left, right), **or**
- Place one of their walls on the board (horizontally, vertically).

**Key rules:**
- Pawns can jump over the opponent if they are adjacent (in case no wall blocks the jump).
- If a straight jump is blocked, the pawn may move diagonally around the opponent.
- Walls are 2 cells long; they cannot overlap, cross existing walls, or completely cut off either player's path to their goal.

---

## Screenshots

| Game Board | Win Screen |
|:---:|:---:|
| ![Game Board](Screenshots/board_game.png) | ![Win Screen](Screenshots/win_screen.png) | | ![Controls](Screenshots/controls.png) | ![In Game](Screenshots/in_game.png) |

---

## Installation & Setup

### Prerequisites

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Pygame** library

### Install Dependencies

```bash
pip install pygame
```

### Clone the Repository

```bash
git clone https://github.com/zeyad-osamaa/Quoridor-Game-.git
cd quoridor
```

---

## How to Run

```bash
python Main.py
```
The game window will open immediately. No additional configuration is required.

---

## Controls

| Input | Action |
|---|---|
| **Arrow Keys** (↑ ↓ ← →) | Move the active pawn one step in any direction |
| **H** | Switch to Horizontal wall placement mode |
| **V** | Switch to Vertical wall placement mode |
| **Left Click** (while in wall mode) | Place a wall at the nearest valid grid position |
| **PvP button** | Switch to Human vs. Human mode (restarts game) |
| **AI button** | Switch to Human vs. AI mode (restarts game) |
| **Easy / Med / Hard buttons** | Change AI difficulty (restarts game) |
| **Restart button** | Reset the board and start a new game |
| **X button** | Quit the application |

> **Wall placement tip:** Press **H** or **V** first to enter wall mode, then click on the edge between two cells where you want place the wall. The status bar will confirm the mode.

---

## Game Modes & AI Difficulty

### Human vs. Human (PvP)
Both players share the same keyboard. Player 1 (red) always moves first.

### Human vs. AI (HvA)
You play as **Player 1 (red)**; the AI controls **Player 2 (blue)**.

| Difficulty | AI Strategy |
|------------|-------------|
|  **Easy**  | 80% random pawn moves, 20% random wall placement — great for beginners. |
| **Medium** | Follows the shortest path to goal; places a strategic wall when the opponent is close to winning. |
|  **Hard**  | Evaluates all possible moves and all wall positions on the board using a heuristic scoring function, choosing the globally best action each turn. |

---

## Project Structure

```
quoridor/
│
├── Main.py    # Game entry point — Pygame loop, rendering, input handling
|__ README.md          
│
└── Assets/
    ├── win.mp3        # Sound when winning
└── game/
    ├── board.py       # Board initialization, Cell class, wall counts
    ├── rules.py       # Movement, wall placement, blocking, path-finding (BFS)
    ├── walls.py       # Wall data class
    ├── ai.py          # AI decision engine (Easy / Medium / Hard)
    └── player.py      # (reserved for future player extensions)
```

---

## References

- Quoridor Official Rules -- [Gigamic Games](https://www.gigamic.com)
- [Pygame Documentation](https://www.pygame.org/docs/)
- Path finding algorithms -- [https://www.redblobgames.com/pathfinding/a-star/introduction.html]
- Python Standard Library -- `collections.deque`, `random`

---

*Developed as a term project for CSE472s: Artificial Intelligence, Ain Shams University — Spring 2026.*
