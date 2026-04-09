import heapq
import time
import pygame

class LocalBeamSolver:
    def __init__(self, maze, beam_width=3):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)
        self.end_pos = self._find_position(3)
        self.beam_width = beam_width
        self.path = []

    def _find_position(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == value:
                    return (i, j)
        return None

    def heuristic(self, pos):
        return abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])

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
        if not self.start_pos or not self.end_pos:
            return []

        beam = [(self.heuristic(self.start_pos), self.start_pos, [self.start_pos])]
        visited = set()
        iterations = 0
        max_iterations = self.rows * self.cols * 2

        while beam and iterations < max_iterations:
            iterations += 1
            next_beam = []

            for heuristic_val, current_pos, path_so_far in beam:
                if step_mode and screen and draw_func:
                    draw_func(current_pos)
                    pygame.display.flip()
                    time.sleep(0.015)

                if current_pos == self.end_pos:
                    self.path = path_so_far
                    return path_so_far

                if current_pos in visited:
                    continue

                visited.add(current_pos)

                for neighbor in self.get_neighbors(current_pos):
                    if neighbor not in visited and neighbor not in path_so_far:
                        new_path = path_so_far + [neighbor]
                        h = self.heuristic(neighbor)
                        next_beam.append((h, neighbor, new_path))

            if not next_beam:
                break

            next_beam.sort(key=lambda x: x[0])
            beam = next_beam[:self.beam_width]

        return []

    def get_maze_with_path(self):
        if not self.path:
            return [row.copy() for row in self.maze]

        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 13
        return maze_copy
