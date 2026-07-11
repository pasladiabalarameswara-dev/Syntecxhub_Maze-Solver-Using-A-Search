# Syntecxhub_Maze-Solver-Using-A-Search
"A Python-based maze solver using the A* Search algorithm to find the shortest path on a coordinate grid, complete with a Manhattan distance heuristic and path visualization. Built for the Syntecxhub internship assignment."

# Syntecxhub Internship - Project 1: Maze Solver using A* Search

This repository contains the implementation of a grid-based Maze Solver using the **A* Search Algorithm**. This project was developed as a required submission for the **Syntecxhub Internship Program**.

---

## 📌 Project Overview
The objective of this project is to model a maze as a grid graph and implement the **A* Search Algorithm** to find the absolute shortest path from a given start node to a designated goal node while effectively routing around walls and managing completely unreachable layouts.

### 🎯 Key Requirements Met:
* **Grid/Node Representation:** The maze layout accurately models the matrix (start, goal, walls) into coordinate nodes.
* **A\* Search with Heuristics:** Implemented using an informed search approach backed by a **Manhattan distance** calculation metric.
* **Shortest Path & Edge Cases:** Safely returns the definitive shortest sequence path or outputs a fallback condition if no mathematical solution path is achievable.
* **Path Visualization:** Outputs graphical layout snapshots representing the agent traversing the generated grid space.

---

## 🧠 Algorithm Mechanics
The algorithm tracks traversal priorities using a Priority Queue based on the core cost evaluation formula:

$$f(n) = g(n) + h(n)$$

Where:
* $g(n)$ is the true path movement cost accrued from the `start` coordinate to the current cell node $n$.
* $h(n)$ is the heuristic estimated distance remaining from node $n$ to the `goal` node, calculated using the Manhattan Distance:

$$|x_1 - x_2| + |y_1 - y_2|$$

---

## 🛠️ Requirements & Installation
The code can be executed smoothly inside cloud notebooks (like Google Colab, Replit) or local environments (like VS Code). 

### Dependencies:
* Python 3.x
* `pyamaze` (Simulation & framework layout rendering)

To run it on your machine, install the package via terminal pipelines:
```bash
pip install pyamaze
