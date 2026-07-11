# Syntecxhub_Maze-Solver-Using-A-Search
"A Python-based maze solver using the A* Search algorithm to find the shortest path on a coordinate grid, complete with a Manhattan distance heuristic and path visualization. Built for the Syntecxhub internship assignment."

# Syntecxhub Internship - Project 1: Maze Solver using A* Search

This repository contains the implementation of a grid-based Maze Solver using the **A* Search Algorithm**. This project was developed as a required submission for the **Syntecxhub Internship Program**.

---

# 🧩 Maze Solver using A* Search

> An intelligent maze-solving engine built with the **A\*** search algorithm — complete with a Python core, console/plot visualization, and an interactive browser-based demo.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white">
  <img alt="Algorithm" src="https://img.shields.io/badge/Algorithm-A*_Search-38BDF8">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow">
  <img alt="Status" src="https://img.shields.io/badge/Status-Complete-4ADE80">
</p>

---

## 📖 Overview

This project models a maze as a grid graph and finds the **shortest path** from a start node to a goal node using the **A\* search algorithm**, guided by a configurable heuristic (Manhattan or Euclidean distance).

Built as part of the **Syntecxhub Internship Program — Project 1**.

---

## ✨ Features

- 🗺️ **Grid-based maze representation** — open cells, walls, start, and goal
- 🧠 **A\* search implementation** — optimal shortest-path guarantee with an admissible heuristic
- 📏 **Configurable heuristics** — switch between Manhattan and Euclidean distance
- ↔️ **4-directional or 8-directional (diagonal) movement**
- 🚫 **Unreachable-goal handling** — fails gracefully instead of crashing
- 🖥️ **Console visualization** — ASCII rendering of explored cells and final path
- 📊 **Plot visualization** — matplotlib image export (`maze_solution.png`)
- 🎮 **Interactive web demo** — animated React visualization of the live search

---

## 🎮 Live Demo

An interactive, animated preview of the algorithm is included at [`demo/astar-maze-preview.jsx`](./demo/astar-maze-preview.jsx). It renders a random maze, animates the A\* frontier expanding node-by-node, then draws the final shortest path.

| Action | What it does |
|---|---|
| **Run A\* Search** | Animates the search frontier and reveals the shortest path |
| **New Maze** | Generates a new random solvable maze |
| **Speed slider** | Controls animation playback speed |

---

## 📁 Project Structure

```
Syntecxhub_Maze_Solver_AStar/
├── maze_solver_astar.py      # Core A* algorithm, maze model, CLI demo
├── demo/
│   └── astar-maze-preview.jsx  # Interactive React visualization
├── maze_solution.png          # Example output (generated on run)
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/Syntecxhub_Maze_Solver_AStar.git
cd Syntecxhub_Maze_Solver_AStar
pip install matplotlib
```

> `matplotlib` is optional — the script runs and prints an ASCII solution without it, but is required for the plotted image.

---

## 🚀 Usage

Run the built-in demo maze:

```bash
python maze_solver_astar.py
```

**Sample output:**

```
=== A* Maze Solver ===

Path found! Length: 19 steps, Cost: 18.00

 S              #
 *  #  #  #     #     #  #
 *  #           #        #
 *  #     #  #  #  #     #
 *  *  *  #              #
 #  #  *  #     #  #  #  #
       *  *  *  #
    #  #  #  *  #     #  #
          #  *  *  *  #
 #  #        .  #  *  *  *  G
```

### Use it in your own code

```python
from maze_solver_astar import Maze, a_star

grid = [
    [0, 0, 0],
    [1, 1, 0],
    [0, 0, 0],
]

maze = Maze(grid, start=(0, 0), goal=(2, 2))
path, explored, cost = a_star(maze, heuristic="manhattan")

if path:
    print(f"Shortest path ({cost} steps): {path}")
else:
    print("Goal is unreachable.")
```

### API reference

| Function / Class | Description |
|---|---|
| `Maze(grid, start, goal)` | Validates and wraps the maze grid |
| `a_star(maze, heuristic, allow_diagonal, verbose)` | Runs A*, returns `(path, explored, cost)` |
| `print_maze(maze, path, explored)` | ASCII console visualization |
| `plot_maze(maze, path, explored)` | Saves a matplotlib PNG of the solved maze |

**Heuristics available:** `"manhattan"` (default, for 4-directional grids) · `"euclidean"` (better suited when diagonal movement is enabled)

---

## 🧠 How A* Works

A\* expands the node in its frontier with the lowest **f(n) = g(n) + h(n)**:

- **g(n)** — exact cost from the start to node `n`
- **h(n)** — heuristic estimate of the remaining cost from `n` to the goal
- **f(n)** — A\*'s priority score; the algorithm always explores the most promising node next

Because the heuristic never overestimates the true cost (it's *admissible*), A\* is guaranteed to return the optimal (shortest) path when one exists.

---

## 🛠️ Tech Stack

- **Python 3** — core algorithm and CLI
- **heapq** — priority queue for the A\* open set
- **matplotlib** — optional plotted visualization
- **React** — interactive browser demo

---

## 👤 Author

Built for the **Syntecxhub Internship Program**.

- 🔗 LinkedIn: mention **@Syntecxhub**
- 💻 GitHub repo name: `Syntecxhub_Maze-Solver-Using-A-Search `

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
