import random
import time
import pygame

class HillClimbingSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)
        self.end_pos = self._find_position(3)
        self.path = []
        self.visited = set()

    def _find_position(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == value:
                    return (i, j)
        return None

    def evaluate(self, pos):
        base_dist = abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])
        val = self.maze[pos[0]][pos[1]]
        if val == 4:
            return base_dist + 10
        elif val == 5:
            return base_dist + 5
        elif val == 6:
            return base_dist + 2
        return base_dist

    def get_neighbors(self, pos):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            ni, nj = pos[0] + di, pos[1] + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols and self.maze[ni][nj] != 1:
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

    def solve(self, step_mode=False, screen=None, draw_func=None, max_iterations=1000, escape_chance=0.2): # chance del 20% per la componente stocastica
        if not self.start_pos or not self.end_pos:
            return []

        current = self.start_pos
        self.path = [current]
        self.visited = {current}

        for _ in range(max_iterations):
            if current == self.end_pos:
                return self.path

            if step_mode and screen and draw_func:
                draw_func(current)
                pygame.display.flip()
                time.sleep(0.015)

            neighbors = [n for n, _ in self.get_neighbors(current) if n not in self.visited]
            if not neighbors:
                break

            best_neighbor = min(neighbors, key=lambda x: self.evaluate(x)) # funzione che minimizza, ossia che valuta il minimo tra i vicini valutati

            if self.evaluate(best_neighbor) >= self.evaluate(current):
                for _ in range (2, 15):    # ciclo for aggiunto per iterare automaticamente la componente stocastica dell'HC
                    if random.random() < escape_chance:
                        random_neighbor = random.choice(neighbors)
                        current = random_neighbor
                        self.path.append(current)
                        self.visited.add(current)
                        continue
                    else:
                        break  # Ottimo locale senza salto
            else:
                current = best_neighbor
                self.path.append(current)
                self.visited.add(current)

        return self.path if current == self.end_pos else []


    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 8  # Valore 8 dalla lista di colori di Visualizza Labirinto
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
