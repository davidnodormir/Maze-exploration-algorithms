from random import choice
import numpy as np

class MazeGenerator:
    def __init__(self, size=51):  
        self.size = size
        self.cell_size = 8
        
        # Inizializza griglia: tutto muri
        self.maze = [['w' for _ in range(size)] for _ in range(size)]
        self.generate_maze()

    def generate_maze(self):
        """Genera il labirinto usando Recursive Backtracking"""
        self.maze = [['w' for _ in range(self.size)] for _ in range(self.size)]
        
        start_row, start_col = 1, 1  # sempre dispari
        self.maze[start_row][start_col] = 'P'
        stack = [(start_row, start_col)]
        
        while stack:
            current_row, current_col = stack[-1]
            neighbors = self.get_valid_neighbors(current_row, current_col)
            
            if neighbors:
                next_row, next_col = choice(neighbors)
                wall_row = (current_row + next_row) // 2
                wall_col = (current_col + next_col) // 2
                self.maze[next_row][next_col] = 'P'
                self.maze[wall_row][wall_col] = 'P'
                stack.append((next_row, next_col))
            else:
                stack.pop()
        
        self.maze[1][1] = 'S'  # Start
        self.maze[self.size-2][self.size-2] = 'E'  # End
        
        # Aggiunge ostacoli
        self.add_obstacles()
        
    def get_valid_neighbors(self, row, col):
        """Trova vicini validi (non visitati) a distanza 2"""
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 < new_row < self.size-1 and 
                0 < new_col < self.size-1 and 
                self.maze[new_row][new_col] == 'w'):
                neighbors.append((new_row, new_col))
        return neighbors
    
    def get_wall_cells(self):
        """Trova tutte le celle muro disponibili per sostituzioni (escluso il contorno)"""
        wall_cells = []
        for row in range(1, self.size-1):  # Escludi prima e ultima riga
            for col in range(1, self.size-1):  # Escludi prima e ultima colonna
                if self.maze[row][col] == 'w':  
                    wall_cells.append((row, col))
        return wall_cells
    
    def add_obstacles(self):
        """Sostituisce 2 muri di ogni tipo con ostacoli"""
        wall_cells = self.get_wall_cells()
        
        # Tipo di ostacolo - Qta aggiunta
        obstacles = [
            ('M', 2),  # Melma
            ('I', 2),  # Muro Illusione  
            ('F', 2)   # Frutto della Dimenticanza
        ]
        
        # Aggiunta degli ostacoli
        # Cerca delle celle muro e vi inserisce gli ostacoli.
        # 2 ostacoli per ogni tipo
        for obstacle_type, count in obstacles:
            for _ in range(count):
                if wall_cells:  
                    chosen_cell = choice(wall_cells)
                    row, col = chosen_cell
                    
                    self.maze[row][col] = obstacle_type
                    
                    wall_cells.remove(chosen_cell)
    
    def maze_to_matrix(self):
        """Converte il labirinto in matrice numerica"""
        mapping = {
            'w': 1,    # Muro
            'P': 0,    # Percorso
            'S': 2,    # Start
            'E': 3,    # End
            'sol': 4,  # Soluzione
            'M': 4,    # Melma
            'I': 5,    # Muro Illusione
            'F': 6     # Frutto della Dimenticanza
        }
        return [[mapping.get(cell, 0) for cell in row] for row in self.maze]

    def save_maze_txt(self, filename):
        """Salva labirinto in un file di testo"""
        try:
            matrix = self.maze_to_matrix()
            with open(filename, 'w') as f:
                for row in matrix:
                    f.write(' '.join(map(str, row)) + '\n')
            print(f"Labirinto salvato in {filename}")
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")

    def print_obstacle_legend(self):
        """Stampa la legenda degli ostacoli"""
        print("=== LEGENDA OSTACOLI ===")
        print("M = Melma (4)")
        print("I = Muro Illusione (5)")  
        print("F = Frutto della Dimenticanza (6)")
        print("S = Start (2)")
        print("E = End (3)")
        print("P = Percorso libero (0)")
        print("w = Muro (1)")
        print("========================")

    def __str__(self):
        """Stampa il labirinto in modo leggibile"""
        return '\n'.join(''.join(row) for row in self.maze)


if __name__ == "__main__":
    print("Generatore di labirinto con ostacoli")
    maze_gen = MazeGenerator(200)
    maze_gen.print_obstacle_legend()
    maze_gen.save_maze_txt("lp.txt")