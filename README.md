# SLE-3: Interactive Maze Solver & Pathfinding System

**Course:** 02AML204 – Introduction to Artificial Intelligence  
**PRN:** 25UAM070  
**Name:** Krisha Champalal Shaha  
**Division:** A

## 1. Project overview

This command-line program finds a path through a 2D grid maze. The user selects the grid size, start and goal coordinates, blocked cells, and a search algorithm. It supports:

- **BFS (Breadth-First Search):** explores in FIFO order and finds a shortest path when each move has equal cost.
- **DFS (Depth-First Search):** explores in LIFO order; it may find a path, but does not guarantee the shortest one.
- **A** Search:* prioritizes nodes using (f(n)=g(n)+h(n)), with Manhattan distance as the heuristic.

The program reports the path, path cost (number of moves), nodes explored, and execution time. It uses only Python's standard library.

## 2. Repository files

- `maze_solver.py` — runnable implementation of the maze problem and the three search algorithms.
- `ARCHITECTURE.md` — C4-style system context, containers, search-engine components, and code-level mapping.
- `AI_Contribution_Log.md` — transparent record of AI assistance and work to verify.

## 3. Run the program

Python 3.10 or newer is recommended.

```bash
python3 maze_solver.py
```

On Windows, this may also work:

```powershell
python maze_solver.py
```

Follow the prompts. Coordinates use **row,column**, starting at **0,0**. For example, a 5-by-5 grid has rows and columns from 0 to 4. Enter blocked cells as comma-separated coordinates such as `1,2; 2,2; 3,2`, or press Enter for no obstacles.

Example configuration:
- Grid size: `5 5`
- Start: `0,0`
- Goal: `4,4`
- Obstacles: `1,2; 2,2; 3,2`
- Algorithm: `BFS`

The exact path and timing depend on the selected algorithm and input. Run the program yourself and use your actual output for screenshots or reports.

## 4. Design notes

- A state is a grid coordinate `(row, column)`.
- Legal actions move **Up, Down, Left, or Right**.
- A cell is valid if it is inside the grid and not an obstacle.
- BFS and DFS use a frontier queue/stack. A* uses a priority queue from `heapq`.
- A visited set avoids repeatedly adding or expanding the same coordinate.
- Manhattan distance is `abs(row1-row2) + abs(col1-col2)`. It is suitable for four-directional movement when every move costs 1.

## 5. Limitations

This is a small educational CLI implementation, not a graphical maze visualizer. All moves have equal cost. A* is optimal for this grid when using the Manhattan heuristic and these movement rules. Runtime values are machine- and input-dependent, so no fixed benchmark is claimed.

