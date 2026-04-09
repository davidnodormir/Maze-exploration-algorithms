
import heapq
import time
import pygame

class UniformCostSolver:
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
                    val = self.maze[ni][nj] #definizione dei vari costi
                    if val == 0: #cella semplice
                        cost = 1
                    elif val == 4: #melma
                        cost = 50
                    elif val == 5: #muro invisibile
                        cost = 10
                    elif val == 6: #frutto della dimenticanza
                        cost = 15
                    else:
                        cost = 1
                    neighbors.append(((ni, nj), cost))
        return neighbors

    def solve(self, step_mode=False, screen=None, draw_func=None):
        heap = []
        heapq.heappush(heap, (0, self.start_pos))
        cost_so_far = {self.start_pos: 0} #si parte dall'inizio con costo zero
        came_from = {self.start_pos: None}

        while heap:
            current_cost, current_pos = heapq.heappop(heap)

            if step_mode and screen and draw_func:
                draw_func(current_pos)
                pygame.display.flip()
                time.sleep(0.015)

            if current_pos == self.end_pos: #se siamo alla fine si ferma
                break

            for neighbor, move_cost in self.get_neighbors(current_pos):
                new_cost = cost_so_far[current_pos] + move_cost #costo per arrivare a current + costo per arrivare al vicino
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]: #verifica del costo minore
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor)) #lo aggiunge
                    came_from[neighbor] = current_pos #aggiorna la posizione

        if self.end_pos in came_from:
            self.path = []
            current = self.end_pos
            while current:
                self.path.append(current)
                current = came_from[current]
            self.path.reverse() #ricostruisce il percorso
            return self.path
        else:
            return []

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 10 #percorso evidenziato in bordeaux
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
                    total_cost += cost #crea il costo totale
                    break
        return total_cost
