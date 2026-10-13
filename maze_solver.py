"""Interactive Maze Solver & Pathfinding System (SLE-3).

Supports Breadth-First Search (BFS), Depth-First Search (DFS), and A*.
Coordinates are (row, column); legal moves are Up, Down, Left, and Right.
Uses only Python's standard library.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
from typing import Callable, Iterable

Position = tuple[int, int]


@dataclass(frozen=True)
class MazeProblem:
    rows: int
    cols: int
    start: Position
    goal: Position
    walls: frozenset[Position]

    def is_valid(self, position: Position) -> bool:
        row, col = position
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and position not in self.walls
        )

    def get_neighbors(self, position: Position) -> list[Position]:
        row, col = position
        # Fixed ordering makes example runs easier to follow.
        candidates = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1),  # Right
        ]
        return [p for p in candidates if self.is_valid(p)]


@dataclass
class SearchResult:
    algorithm: str
    path: list[Position] | None
    nodes_explored: int
    elapsed_ms: float

    @property
    def path_cost(self) -> int | None:
        return len(self.path) - 1 if self.path else None


def reconstruct_path(
    parent: dict[Position, Position | None], goal: Position
) -> list[Position]:
    path: list[Position] = []
    current: Position | None = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def heuristic(position: Position, goal: Position) -> int:
    """Manhattan distance for four-directional, unit-cost movement."""
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def solve_bfs(problem: MazeProblem) -> tuple[list[Position] | None, int]:
    frontier = deque([problem.start])
    parent: dict[Position, Position | None] = {problem.start: None}
    visited = {problem.start}
    explored = 0

    while frontier:
        current = frontier.popleft()
        explored += 1
        if current == problem.goal:
            return reconstruct_path(parent, current), explored

        for neighbor in problem.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                frontier.append(neighbor)

    return None, explored


def solve_dfs(problem: MazeProblem) -> tuple[list[Position] | None, int]:
    frontier = [problem.start]
    parent: dict[Position, Position | None] = {problem.start: None}
    visited = {problem.start}
    explored = 0

    while frontier:
        current = frontier.pop()
        explored += 1
        if current == problem.goal:
            return reconstruct_path(parent, current), explored

        for neighbor in problem.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                frontier.append(neighbor)

    return None, explored


def solve_astar(problem: MazeProblem) -> tuple[list[Position] | None, int]:
    sequence = count()
    frontier: list[tuple[int, int, int, Position]] = []
    heappush(frontier, (heuristic(problem.start, problem.goal), 0, next(sequence), problem.start))
    parent: dict[Position, Position | None] = {problem.start: None}
    g_score = {problem.start: 0}
    closed: set[Position] = set()
    explored = 0

    while frontier:
        _, cost, _, current = heappop(frontier)

        # Ignore stale queue entries and states already fully processed.
        if cost != g_score.get(current) or current in closed:
            continue

        closed.add(current)
        explored += 1
        if current == problem.goal:
            return reconstruct_path(parent, current), explored

        for neighbor in problem.get_neighbors(current):
            tentative_g = cost + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                f_score = tentative_g + heuristic(neighbor, problem.goal)
                heappush(frontier, (f_score, tentative_g, next(sequence), neighbor))

    return None, explored


SOLVERS: dict[str, Callable[[MazeProblem], tuple[list[Position] | None, int]]] = {
    "BFS": solve_bfs,
    "DFS": solve_dfs,
    "ASTAR": solve_astar,
    "A*": solve_astar,
}


def run_search(problem: MazeProblem, algorithm: str) -> SearchResult:
    key = algorithm.strip().upper()
    if key not in SOLVERS:
        raise ValueError("Choose BFS, DFS, or A*.")
    start_time = perf_counter()
    path, explored = SOLVERS[key](problem)
    elapsed_ms = (perf_counter() - start_time) * 1000
    display_name = "A*" if key in {"ASTAR", "A*"} else key
    return SearchResult(display_name, path, explored, elapsed_ms)


def parse_position(value: str) -> Position:
    pieces = value.strip().replace(" ", "").split(",")
    if len(pieces) != 2:
        raise ValueError("Enter coordinates as row,column (example: 0,3).")
    return int(pieces[0]), int(pieces[1])


def parse_walls(value: str) -> frozenset[Position]:
    if not value.strip():
        return frozenset()
    return frozenset(parse_position(item) for item in value.split(";") if item.strip())


def display_maze(problem: MazeProblem, path: Iterable[Position] | None = None) -> None:
    path_cells = set(path or [])
    for row in range(problem.rows):
        symbols = []
        for col in range(problem.cols):
            pos = (row, col)
            if pos == problem.start:
                symbol = "S"
            elif pos == problem.goal:
                symbol = "G"
            elif pos in problem.walls:
                symbol = "#"
            elif pos in path_cells:
                symbol = "*"
            else:
                symbol = "."
            symbols.append(symbol)
        print(" ".join(symbols))
    print("Legend: S=start, G=goal, #=obstacle, *=path, .=open cell")


def read_positive_int(prompt: str) -> int:
    value = int(input(prompt))
    if value <= 0:
        raise ValueError("Grid dimensions must be positive integers.")
    return value


def main() -> None:
    print("=== Interactive Maze Solver ===")
    try:
        rows = read_positive_int("Number of rows: ")
        cols = read_positive_int("Number of columns: ")
        start = parse_position(input("Start coordinate (row,column): "))
        goal = parse_position(input("Goal coordinate (row,column): "))
        walls = parse_walls(
            input("Obstacle coordinates separated by ';' (or press Enter): ")
        )
        algorithm = input("Algorithm (BFS / DFS / A*): ").strip().upper()

        problem = MazeProblem(rows, cols, start, goal, walls)
        if not problem.is_valid(start):
            raise ValueError("Start must be inside the grid and not an obstacle.")
        if not problem.is_valid(goal):
            raise ValueError("Goal must be inside the grid and not an obstacle.")
        if start == goal:
            # All algorithms correctly return the one-cell path.
            pass

        print("\nMaze:")
        display_maze(problem)
        result = run_search(problem, algorithm)

        print(f"\nAlgorithm: {result.algorithm}")
        if result.path is None:
            print("Result: No path found.")
        else:
            print("Result: Path found.")
            print("Path:", " -> ".join(f"({r},{c})" for r, c in result.path))
            print("Path cost (moves):", result.path_cost)
            print("\nMaze with path:")
            display_maze(problem, result.path)

        print("Nodes explored:", result.nodes_explored)
        print(f"Execution time: {result.elapsed_ms:.6f} ms")

    except (ValueError, EOFError) as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
