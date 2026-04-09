import random
import math
import pygame
import time

class SimulatedAnnealingSolver:
    def __init__(self, maze, initial_temp=1000, cooling_rate=0.995, min_temp=0.1):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)
        self.end_pos = self._find_position(3)
        self.path = []
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate #tasso di raffreddamento
        self.min_temp = min_temp #temperatura minima, al di sotto la ricerca si blocca 

        #costi come nell' UCS
        self.cell_cost = {
            0: 1,    # cella semplice
            2: 0,    # partenza
            3: 0,    # arrivo
            4: 50,   # frutto della dimenticanza
            5: 10,   # muro invisibile
            6: 15,   # melma
        }

    def _find_position(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == value:
                    return (i, j)
        return None

    def get_neighbors(self, pos):
        neighbors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for di, dj in directions:
            ni, nj = pos[0] + di, pos[1] + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols: #verifica di essere ancora nei confini
                cell_val = self.maze[ni][nj]
                if cell_val != 1:  #muro
                    cost = self.cell_cost.get(cell_val, 1)
                    neighbors.append(((ni, nj), cost))
        return neighbors

    def evaluate(self, pos):
        #euristica : distanza + costo della cella
        base_dist = abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])
        penalty = self.cell_cost.get(self.maze[pos[0]][pos[1]], 1)
        return base_dist + penalty

    def solve(self, step_mode=False, screen=None, draw_func=None):
        current = self.start_pos
        current_eval = self.evaluate(current)
        temperature = self.initial_temp
        path = [current]
        visited = set([current])

        while temperature > self.min_temp:
            neighbors = self.get_neighbors(current)
            if not neighbors:
                break

            next_pos, move_cost = random.choice(neighbors) 
            next_eval = self.evaluate(next_pos)
            delta = next_eval - current_eval #calcolo di deltaE

            #probabilità per accettare lo spostamento
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current = next_pos
                current_eval = next_eval
                path.append(current)
                visited.add(current)

            temperature *= self.cooling_rate #aggiorna la temperatura seconod il tasso

            if step_mode and draw_func and screen:
                draw_func(current)
                pygame.display.flip()
                time.sleep(0.015)

            if current == self.end_pos:
                break

        self.path = path
        return path

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 12  # percorso giallo
        return maze_copy

    def get_path_cost(self):
        if not self.path:
            return float('inf') #restituisce infinito se non c'è il percorso
        total_cost = 0
        for i in range(1, len(self.path)):
            prev = self.path[i - 1]
            curr = self.path[i]
            for neighbor, cost in self.get_neighbors(prev):
                if neighbor == curr:
                    total_cost += cost
                    break
        return total_cost
