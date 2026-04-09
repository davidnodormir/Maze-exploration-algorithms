from collections import deque
import time
import pygame

class BreadthFirstSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)
        self.end_pos = self._find_position(3)
        self.path = []

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
                    neighbors.append((ni, nj))
        return neighbors

    def solve(self, step_mode=False, screen=None, draw_func=None):
        queue = deque([self.start_pos])
        visited = {self.start_pos}
        came_from = {self.start_pos: None}

        while queue:
            current = queue.popleft()

            # Visualizzazione passo-passo
            if step_mode and screen and draw_func:
                draw_func(current)
                pygame.display.flip()
                time.sleep(0.015)

            if current == self.end_pos:
                path = []
                while current != self.start_pos:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start_pos)
                path.reverse()
                self.path = path
                return path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return []

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 14  
        return maze_copy
