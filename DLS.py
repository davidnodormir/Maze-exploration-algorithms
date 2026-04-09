import time
import pygame

class DLSSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)
        self.end_pos = self._find_position(3)
        self.path = []
        self.cutoff_occurred = False

    def _find_position(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == value:
                    return (i, j)
        return None

    def get_neighbors(self, pos):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            ni, nj = pos[0] + di, pos[1] + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                if self.maze[ni][nj] != 1:
                    val = self.maze[ni][nj]
                    if val == 0:
                        cost = 1
                    elif val == 4:
                        cost = 3
                    elif val == 5:
                        cost = 5
                    elif val == 6:
                        cost = 2
                    else:
                        cost = 1
                    neighbors.append(((ni, nj), cost))
        return neighbors

    def recursive_dls(self, node, limit, depth, current_path, visited, step_mode, screen, draw_func):
        if node == self.end_pos:
            self.path = current_path + [node]
            return "success"
        elif depth == limit:
            self.cutoff_occurred = True
            return "cutoff"

        if step_mode and screen and draw_func:
            draw_func(node)
            pygame.display.flip()
            time.sleep(0.015)

        cutoff = False
        for neighbor, _ in self.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                result = self.recursive_dls(
                    neighbor, limit, depth + 1, current_path + [node],
                    visited, step_mode, screen, draw_func
                )
                if result == "success":
                    return result
                elif result == "cutoff":
                    cutoff = True

        return "cutoff" if cutoff else "failure"

    def solve(self, step_mode=False, screen=None, draw_func=None, limit=10):
        if not self.start_pos or not self.end_pos:
            return []

        self.cutoff_occurred = False
        visited = {self.start_pos}
        result = self.recursive_dls(self.start_pos, limit, 0, [], visited, step_mode, screen, draw_func)

        if result == "success":
            return self.path
        elif result == "cutoff":
            print(f"Attenzione: Raggiunto il limite di profondità {limit} senza trovare la soluzione")
        return []

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 9  # Valore 9 dalla lista di colori di Visualizza Labirinto
        return maze_copy

    def get_path_cost(self):
        if not self.path:
            return float('inf')
        total_cost = 0
        for i in range(1, len(self.path)):
            prev = self.path[i - 1]
            curr = self.path[i]
            for neighbor, cost in self.get_neighbors(prev):
                if neighbor == curr:
                    total_cost += cost
                    break
        return total_cost
