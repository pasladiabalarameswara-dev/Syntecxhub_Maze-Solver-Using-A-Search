"""
Maze Solver using A* Search
============================
Represents a maze/grid (start, goal, walls), models it as nodes,
implements A* search with a configurable heuristic (Manhattan or
Euclidean), returns the shortest path, handles unreachable cases,
and optionally visualizes the search and final path (console + plot).

Usage:
    python maze_solver_astar.py
"""

import heapq
import math

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ---------------------------------------------------------------------
# Node representation
# ---------------------------------------------------------------------
class Node:
    """A single cell/node in the maze grid."""

    __slots__ = ("row", "col", "g", "h", "f", "parent")

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = float("inf")   # cost from start to this node
        self.h = 0.0             # heuristic estimate to goal
        self.f = float("inf")   # g + h
        self.parent = None

    @property
    def pos(self):
        return (self.row, self.col)

    def __lt__(self, other):
        # Tie-breaking on f, then h, keeps the heap well-ordered
        return (self.f, self.h) < (other.f, other.h)

    def __eq__(self, other):
        return isinstance(other, Node) and self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)


# ---------------------------------------------------------------------
# Maze representation
# ---------------------------------------------------------------------
class Maze:
    """
    Grid-based maze.
    0 = open cell, 1 = wall.
    """

    def __init__(self, grid, start, goal):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.start = start
        self.goal = goal

        if not self._in_bounds(*start) or not self._in_bounds(*goal):
            raise ValueError("Start or goal is outside the maze bounds.")
        if self.grid[start[0]][start[1]] == 1:
            raise ValueError("Start position is on a wall.")
        if self.grid[goal[0]][goal[1]] == 1:
            raise ValueError("Goal position is on a wall.")

    def _in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row, col):
        return self._in_bounds(row, col) and self.grid[row][col] == 0

    def neighbors(self, row, col, allow_diagonal=False):
        """Return walkable neighbor coordinates (4- or 8-directional)."""
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if allow_diagonal:
            moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        result = []
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if self.is_walkable(nr, nc):
                # For diagonal moves, prevent cutting through wall corners
                if allow_diagonal and dr != 0 and dc != 0:
                    if not self.is_walkable(row + dr, col) and not self.is_walkable(row, col + dc):
                        continue
                cost = math.sqrt(2) if (dr != 0 and dc != 0) else 1
                result.append(((nr, nc), cost))
        return result


# ---------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


HEURISTICS = {
    "manhattan": manhattan,
    "euclidean": euclidean,
}


# ---------------------------------------------------------------------
# A* Search
# ---------------------------------------------------------------------
def a_star(maze, heuristic="manhattan", allow_diagonal=False, verbose=False):
    """
    Run A* search on the given Maze.

    Returns:
        path (list of (row, col)) or None if unreachable
        explored (set of (row, col)) - nodes visited, for visualization
        cost (float) - total path cost, or None if unreachable
    """
    if heuristic not in HEURISTICS:
        raise ValueError(f"Unknown heuristic '{heuristic}'. Use one of {list(HEURISTICS)}.")
    h_func = HEURISTICS[heuristic]

    start, goal = maze.start, maze.goal

    nodes = {}
    def get_node(pos):
        if pos not in nodes:
            nodes[pos] = Node(*pos)
        return nodes[pos]

    start_node = get_node(start)
    start_node.g = 0
    start_node.h = h_func(start, goal)
    start_node.f = start_node.h

    open_heap = []
    heapq.heappush(open_heap, start_node)
    open_set = {start: start_node}
    closed_set = set()
    explored_order = []

    step = 0
    while open_heap:
        current = heapq.heappop(open_heap)

        if current.pos in closed_set:
            continue

        closed_set.add(current.pos)
        explored_order.append(current.pos)
        step += 1

        if verbose:
            print(f"Step {step}: exploring {current.pos}  g={current.g:.2f} h={current.h:.2f} f={current.f:.2f}")

        if current.pos == goal:
            path = _reconstruct_path(current)
            return path, closed_set, current.g

        for neighbor_pos, move_cost in maze.neighbors(current.row, current.col, allow_diagonal):
            if neighbor_pos in closed_set:
                continue

            neighbor = get_node(neighbor_pos)
            tentative_g = current.g + move_cost

            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = h_func(neighbor_pos, goal)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(open_heap, neighbor)
                open_set[neighbor_pos] = neighbor

    # Goal never reached -> unreachable
    return None, closed_set, None


def _reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node.pos)
        node = node.parent
    path.reverse()
    return path


# ---------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------
def print_maze(maze, path=None, explored=None):
    """Console visualization of the maze, explored cells, and final path."""
    path_set = set(path) if path else set()
    explored_set = explored or set()

    for r in range(maze.rows):
        row_str = ""
        for c in range(maze.cols):
            pos = (r, c)
            if pos == maze.start:
                row_str += " S "
            elif pos == maze.goal:
                row_str += " G "
            elif maze.grid[r][c] == 1:
                row_str += " # "
            elif pos in path_set:
                row_str += " * "
            elif pos in explored_set:
                row_str += " . "
            else:
                row_str += "   "
        print(row_str)
    print()


def plot_maze(maze, path=None, explored=None, title="A* Maze Solver"):
    """Matplotlib visualization (optional)."""
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib not installed; skipping plot visualization.")
        return

    fig, ax = plt.subplots(figsize=(maze.cols / 2, maze.rows / 2))

    # Draw grid cells
    for r in range(maze.rows):
        for c in range(maze.cols):
            color = "white"
            if maze.grid[r][c] == 1:
                color = "black"
            elif explored and (r, c) in explored:
                color = "#cfe8ff"  # light blue for explored
            rect = patches.Rectangle((c, maze.rows - 1 - r), 1, 1,
                                      facecolor=color, edgecolor="gray", linewidth=0.5)
            ax.add_patch(rect)

    # Draw path
    if path:
        for (r, c) in path:
            rect = patches.Rectangle((c, maze.rows - 1 - r), 1, 1,
                                      facecolor="#ffd54f", edgecolor="gray", linewidth=0.5)
            ax.add_patch(rect)

    # Start / goal markers
    sr, sc = maze.start
    gr, gc = maze.goal
    ax.add_patch(patches.Rectangle((sc, maze.rows - 1 - sr), 1, 1, facecolor="green"))
    ax.add_patch(patches.Rectangle((gc, maze.rows - 1 - gr), 1, 1, facecolor="red"))

    ax.set_xlim(0, maze.cols)
    ax.set_ylim(0, maze.rows)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig("maze_solution.png", dpi=150)
    print("Plot saved to maze_solution.png")
    plt.show()


# ---------------------------------------------------------------------
# Demo / main
# ---------------------------------------------------------------------
def main():
    # 0 = open, 1 = wall
    grid = [
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    ]

    start = (0, 0)
    goal = (9, 9)

    maze = Maze(grid, start, goal)

    path, explored, cost = a_star(maze, heuristic="manhattan", allow_diagonal=False, verbose=False)

    print("=== A* Maze Solver ===\n")
    if path is None:
        print("No path found. The goal is unreachable from the start.")
        print_maze(maze, explored=explored)
    else:
        print(f"Path found! Length: {len(path)} steps, Cost: {cost:.2f}\n")
        print("Path:", path, "\n")
        print_maze(maze, path=path, explored=explored)
        plot_maze(maze, path=path, explored=explored)


if __name__ == "__main__":
    main()
