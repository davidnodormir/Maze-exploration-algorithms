import heapq
import time
import pygame

class GreedySolver:
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

    def heuristic(self, pos):
        return abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])

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

    def solve(self, step_mode=False, screen=None, draw_func=None):
        if not self.start_pos or not self.end_pos:
            return []

        open_list = []
        heapq.heappush(open_list, (self.heuristic(self.start_pos), self.start_pos))
        came_from = {self.start_pos: None}
        visited = set()

        while open_list:
            _, current = heapq.heappop(open_list)

            if step_mode and screen and draw_func:
                draw_func(current)
                pygame.display.flip()
                time.sleep(0.015)

            if current == self.end_pos:
                break

            visited.add(current)

            for neighbor, _ in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_list, (self.heuristic(neighbor), neighbor))

        if self.end_pos in came_from:
            self.path = []
            current = self.end_pos
            while current:
                self.path.append(current)
                current = came_from[current]
            self.path.reverse()
            return self.path
        else:
            return []

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 7  # Valore 7 dalla lista di colori di Visualizza Labirinto
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
