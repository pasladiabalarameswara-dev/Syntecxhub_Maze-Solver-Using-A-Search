import subprocess
import sys
from queue import PriorityQueue

try:
    from pyamaze import maze, agent, textLabel
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyamaze"])
    from pyamaze import maze, agent, textLabel

def h(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def aStar(m):
    start = (m.rows, m.cols)
    goal = (1, 1)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)
    
    open_queue = PriorityQueue()
    open_queue.put((f_score[start], h(start, goal), start))
    aPath = {}
    
    while not open_queue.empty():
        currCell = open_queue.get()[2]
        if currCell == goal:
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d] == 1:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W': childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N': childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S': childCell = (currCell[0] + 1, currCell[1])
                
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, goal)
                
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open_queue.put((temp_f_score, h(childCell, goal), childCell))
                    aPath[childCell] = currCell
    fwdPath = {}
    cell = goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return fwdPath

if __name__ == '__main__':
    m = maze(10, 15)
    m.createMaze()
    path = aStar(m)
    a = agent(m, footprints=True, color='red')
    textLabel(m, 'A* Path Length', len(path) + 1)
    m.tracePath({a: path})
    m.run(saveMovie=True)

