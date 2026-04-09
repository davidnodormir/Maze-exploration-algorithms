import heapq
import time
import pygame

class AStarSolver:
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

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  #euristica considerata:distanza di Manhattan

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
        open_set = []
        heapq.heappush(open_set, (0, self.start_pos))
        came_from = {self.start_pos: None} #parte dall'inizio con costo 0
        g_score = {self.start_pos: 0}

        while open_set:
            _, current = heapq.heappop(open_set) #estrae una cella dalla coda

            if step_mode and screen and draw_func: #e lo stampa a video
                draw_func(current)
                pygame.display.flip()
                time.sleep(0.015)

            if current == self.end_pos: #se è l'ultima cella allora si blocca
                break

            for neighbor, move_cost in self.get_neighbors(current):
                tentative_g = g_score[current] + move_cost #costo fatto finora + costo per raggiungere il vicino
                if neighbor not in g_score or tentative_g < g_score[neighbor]:  #se il vicino non è stato visto o se è stato trovato un percorso più economico
                    g_score[neighbor] = tentative_g
                    priority = tentative_g + self.heuristic(neighbor, self.end_pos) #g()+h()
                    heapq.heappush(open_set, (priority, neighbor)) ##inserisce il vicino nella coda di priorità, ordinata per f()
                    came_from[neighbor] = current

        if self.end_pos in came_from: #funzione che costruisce il percorso dalla fine all'inzio
            self.path = []
            current = self.end_pos
            while current:
                self.path.append(current)
                current = came_from[current]
            self.path.reverse() #viene inverito
            return self.path
        else:
            return []

    def get_maze_with_path(self):
        if not self.path:
            return self.maze
        maze_copy = [row.copy() for row in self.maze]
        for i, j in self.path:
            if maze_copy[i][j] not in (2, 3):
                maze_copy[i][j] = 11  #percorso in violetto
        return maze_copy

    def get_path_cost(self):
        if not self.path:
            return float('inf') #se non esiste il percorso restituisce infinito
        total_cost = 0
        for i in range(1, len(self.path)):
            prev = self.path[i - 1]
            curr = self.path[i]
            for neighbor, cost in self.get_neighbors(prev):
                if neighbor == curr:
                    total_cost += cost #prende il costo del vicino e lo somma
                    break
        return total_cost
