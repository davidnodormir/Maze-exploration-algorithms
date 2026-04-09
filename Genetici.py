import random
from collections import deque

class GeneticMazeSolver:
    def __init__(self, maze, population_size=100, max_generations=200, mutation_rate=0.1):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start_pos = self._find_position(2)  
        self.end_pos = self._find_position(3)    
        
        # Parametri algoritmo genetico
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.elite_rate = 0.1  # 10% migliori individui
        self.cull_rate = 0.1   # 10% peggiori individui da eliminare
        
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.direction_names = ['U', 'D', 'L', 'R']
        
        #Stima della lunghezza massima del percorso
        if self.start_pos and self.end_pos:
            manhattan_dist = abs(self.start_pos[0] - self.end_pos[0]) + abs(self.start_pos[1] - self.end_pos[1])
            
            #Da def dovrebbe essere tre, provando a moltiplicare per numeri differenti, ho notato che raggiunge la soluzione facendo *20
            
            self.max_path_length = min(manhattan_dist * 5, self.rows * self.cols)
        else:
            self.max_path_length = self.rows * self.cols
        
        self.best_path = []
        self.best_fitness = 0

    def _find_position(self, value):
        """Trova la posizione di un valore specifico nella matrice."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == value:
                    return (i, j)
        return None

    def manhattan_distance(self, pos1, pos2):
        """Calcola la distanza di Manhattan tra due posizioni."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def is_valid_position(self, pos):
        """Verifica se una posizione è valida (dentro i confini e non un muro)."""
        return (0 <= pos[0] < self.rows and 
                0 <= pos[1] < self.cols and 
                self.maze[pos[0]][pos[1]] != 1)

class Individual:
    def __init__(self, chromosome, solver):
        self.chromosome = chromosome  
        self.solver = solver
        self.fitness = 0
        self.path = []
        self.reached_end = False
        self.calculate_fitness()

    @classmethod
    def create_random_individual(cls, solver):
        """Crea un individuo con cromosoma casuale."""
        chromosome = [random.choice(solver.direction_names) 
                     for _ in range(solver.max_path_length)]
        return cls(chromosome, solver)

    def calculate_fitness(self):
        """Calcola il fitness dell'individuo basato sul percorso generato."""
        if not self.solver.start_pos or not self.solver.end_pos:
            self.fitness = 0
            return

        current_pos = self.solver.start_pos
        self.path = [current_pos]
        visited = set([current_pos])
        
        # Esegue le mosse del cromosoma
        for direction in self.chromosome:
            direction_idx = self.solver.direction_names.index(direction)
            move = self.solver.directions[direction_idx]
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            # Se la mossa è valida
            if self.solver.is_valid_position(new_pos):
                current_pos = new_pos
                self.path.append(current_pos)
                
                # Se ha raggiunto la fine
                if current_pos == self.solver.end_pos:
                    self.reached_end = True
                    break
                    
                visited.add(current_pos)
            # Se la mossa non è valida, resta fermo
        
        # Calcolo del fitness
        if self.reached_end:

            #Aggiunge un bonuso di +1000 per aver raggiunto la fine + le penalità per lunghezza percorso
            self.fitness = 1000 + (500 / len(self.path))
        else:
            # Fitness basato sulla vicinanza alla fine
            final_distance = self.solver.manhattan_distance(current_pos, self.solver.end_pos)
            max_distance = self.solver.manhattan_distance(self.solver.start_pos, self.solver.end_pos)
            
            # Il fintness aumenta con la vicinanza alla fine
            if max_distance > 0:
                closeness = (max_distance - final_distance) / max_distance
                self.fitness = closeness * 100
            else:
                self.fitness = 0
            
            
            unique_cells = len(set(self.path))
            self.fitness += unique_cells * 2

    def mutate(self):
        """Muta l'individuo cambiando alcune direzioni casuali."""
        for i in range(len(self.chromosome)):
            if random.random() < self.solver.mutation_rate:
                self.chromosome[i] = random.choice(self.solver.direction_names)
        
        # Ricalcolo del fintness a seguito di una mutazione 
        self.calculate_fitness()

    def crossover(self, partner):
        """Effettua crossover con un altro individuo."""
        child_chromosome = []
        
        for i in range(len(self.chromosome)):
            prob = random.random()
            if prob < 0.45:
                child_chromosome.append(self.chromosome[i])
            elif prob < 0.90:
                child_chromosome.append(partner.chromosome[i])
            else:
                # Mutazione durante crossover
                child_chromosome.append(random.choice(self.solver.direction_names))
        
        return Individual(child_chromosome, self.solver)

def solve_maze_genetic(solver):
    """Risolve il labirinto usando l'algoritmo genetico."""
    if not solver.start_pos or not solver.end_pos:
        return []

    population = [Individual.create_random_individual(solver) 
                 for _ in range(solver.population_size)]
    
    generation = 1
    found = False
    
    print(f"Inizio risoluzione labirinto con algoritmo genetico...")
    print(f"Start: {solver.start_pos}, End: {solver.end_pos}")
    print(f"Parametri: Pop={solver.population_size}, MaxGen={solver.max_generations}")
    
    while not found and generation <= solver.max_generations:
        # Riordina la popolazione per fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        
        if population[0].reached_end:
            found = True
            solver.best_path = population[0].path
            solver.best_fitness = population[0].fitness
            break
        
        #Ad ogni 10 generazioni stampa lo stato raggiunto 
        if generation % 10 == 0 or generation == 1:
            best_individual = population[0]
            print(f"Gen {generation}: Fitness={best_individual.fitness:.2f}, "
                  f"Raggiunto fine: {best_individual.reached_end}, "
                  f"Lunghezza percorso: {len(best_individual.path)}")
        
        # Crea nuova generazione
        new_population = []
        
        # ELITISMO: mantiene la popolazione (impostato a 0.1 prende il 10% migliore)
        elite_count = int(solver.elite_rate * solver.population_size)
        new_population.extend(population[:elite_count])
        
        # CULLING: elimina la parte peggiore della popolazione 
        cull_count = int(solver.cull_rate * solver.population_size)
        population = population[:-cull_count] if cull_count > 0 else population
        
        # Genera resto della popolazione tramite crossover
        remaining = solver.population_size - len(new_population)
        
        for _ in range(remaining):
            weights = [max(0.1, ind.fitness) for ind in population]  
            total_weight = sum(weights)
            
            if total_weight > 0:
                weights = [w/total_weight for w in weights]
                parent1, parent2 = random.choices(population, weights=weights, k=2)
            else:
                
                parent1, parent2 = random.choices(population, k=2)
            
            # Crossover e mutazione
            child = parent1.crossover(parent2)
            child.mutate()
            new_population.append(child)
        
        population = new_population
        generation += 1
    
    # Risultati finali
    population.sort(key=lambda x: x.fitness, reverse=True)
    best_individual = population[0]
    
    print(f"\nRisultato finale:")
    print(f"Generazioni: {generation-1}")
    print(f"Soluzione trovata: {best_individual.reached_end}")
    print(f"Fitness migliore: {best_individual.fitness:.2f}")
    print(f"Lunghezza percorso: {len(best_individual.path)}")
    
    if best_individual.reached_end:
        solver.best_path = best_individual.path
        return best_individual.path
    else:
        
        solver.best_path = best_individual.path
        return best_individual.path


def solve(self):
    """Risolve il labirinto usando l'algoritmo genetico."""
    return solve_maze_genetic(self)

def get_maze_with_path(self):
    """Restituisce una copia del labirinto con il percorso evidenziato (valore 7)."""
    if not self.best_path:
        return self.maze

    maze_copy = [row.copy() for row in self.maze]
    for i, j in self.best_path:
        if maze_copy[i][j] not in (2, 3):  
            maze_copy[i][j] = 15
    return maze_copy


GeneticMazeSolver.solve = solve
GeneticMazeSolver.get_maze_with_path = get_maze_with_path

