import pygame
import sys
import os
import time

pygame.init()

WINDOW_SIZE = 800
CELL_SIZE = 30  
BUTTON_PANEL_WIDTH = 500  


# Colori per ogni tipo di cella
COLORS = {
    0: (238, 203, 173),  # Percorso - Sabbia chiaro
    1: (0, 0, 0),        # Muro - Nero
    2: (255, 255, 0),    # Inizio - Giallo
    3: (255, 0, 0),      # Fine - Rosso
    4: (0, 100, 0),      # Melma - Verde scuro
    5: (0, 0, 255),      # MuroIllusione - Blu
    6: (128, 0, 128),     # FruttoDimenticanza - Viola
    # VINCENZO
    7: (0, 255, 0),       # Percorso trovato - Verde brillante
    8: (255, 165, 0),     # Percorso Hill Climbing - Arancione
    9: (0, 191, 255),  # Percorso DLS - Blu chiaro
    #GRAZIA
    10: (165, 42, 42),
    11: (216, 191, 216),
    12: (238, 173, 14),
    #DAVIDE
    13: (153, 50, 204),
    14: (79, 148, 205),
    15: (107, 142, 35)
}

# Nomi descrittivi per debug
CELL_NAMES = {
    0: "Percorso",
    1: "Muro",
    2: "Inizio",
    3: "Fine",
    4: "Melma",
    5: "MuroIllusione",
    6: "FruttoDimenticanza",
    7: "PercorsoTrovato",
    8: "PercorsoHillClimbing",
    9: "PercorsoDLS",
    10: "percorso ucs",
    11: "Percorso A*",
    12: "percorso Simulated annealing",
    13: "Local Beam",
    14: "Ampiezza",
    15: "Genetici"

}

def load_maze_from_file(filename):
    """Carica la matrice del labirinto da un file di testo"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    
    try:
        # Usa file_path invece di filename
        with open(file_path, 'r') as file:
            maze = []
            for line in file:
                line = line.strip()
                if line:  
                    if ' ' in line:
                        row = [int(x) for x in line.split()]
                    else:
                        row = [int(x) for x in line]
                    maze.append(row)
            return maze
    except FileNotFoundError:
        print(f"Errore: File '{file_path}' non trovato!")
    except ValueError as e:
        print(f"Errore nel formato del file: {e}")
        

class Button:
    """Classe per gestire i pulsanti"""
    def __init__(self, x, y, width, height, text, font=None,
                 color=(200, 200, 200), hover_color=(170, 170, 170),
                 press_color=(150, 150, 150), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.hover_color = hover_color
        self.press_color = press_color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont(None, 24)    # DIM FONT           

        self.is_pressed = False
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.rect.collidepoint(event.pos):
                    self.is_pressed = False
                    return "clicked"
                self.is_pressed = False
        return False

    def draw(self, surface):
        # Scegli il colore in base allo stato
        if self.is_pressed:
            color = self.press_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.base_color

        # Disegna il rettangolo
        pygame.draw.rect(surface, color, self.rect, border_radius=8)  

        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2, border_radius=8)  #Ombra contorno

        lines = self.text.split('\n')
        line_height = self.font.get_linesize()
        total_height = len(lines) * line_height
        start_y = self.rect.y + (self.rect.height - total_height) // 2

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, start_y + i * line_height))
            if self.is_pressed:
                text_rect.move_ip(1, 1)
            surface.blit(text_surface, text_rect)

def create_button_grid(start_x, start_y, button_size=120, spacing=15):
    """Crea una griglia 3x3 di pulsanti con nomi personalizzati"""
    buttons = []

    labels = [
        "A*", "Simulated\nAnnealing", "Costo\nuniforme",
        "Greedy", "Hill Climbing", "DLS",
        "Local beam", "In ampiezza", "Genetico"
    ]

    for i in range(3):  
        for j in range(3):  
            index = i * 3 + j
            x = start_x + j * (button_size + spacing)
            y = start_y + i * (button_size + spacing)
            button = Button(x, y, button_size, button_size, labels[index])
            buttons.append(button)

    return buttons

def draw_button_panel(screen, maze_width, window_height, buttons):
    """Disegna il pannello dei pulsanti separato dal labirinto"""
    panel_x = maze_width + 20
    panel_y = 20
    panel_width = BUTTON_PANEL_WIDTH - 40
    panel_height = window_height - 40
    
    # Pannello laterale 167-175
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (240, 240, 240), panel_rect)
    
    pygame.draw.rect(screen, (100, 100, 100), panel_rect, 3)
    
    font_title = pygame.font.Font(None, 28)
    title_text = font_title.render("ALGORITMI", True, (50, 50, 50))
    title_rect = title_text.get_rect(centerx=panel_rect.centerx, y=panel_y + 20)
    screen.blit(title_text, title_rect)
    
    
    line_y = title_rect.bottom + 10
    pygame.draw.line(screen, (150, 150, 150), 
                    (panel_x + 20, line_y), 
                    (panel_x + panel_width - 20, line_y), 2)
    
    
    for button in buttons:
        button.draw(screen)


def draw_maze(screen, maze, maze_width, window_height):
    """Disegna la matrice del labirinto"""
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    
    # Calcola dimensioni ottimali per il labirinto basate sulla finestra
    available_width = maze_width - 40  
    available_height = window_height - 160  
    
    cell_width = available_width // cols if cols > 0 else 20
    cell_height = available_height // rows if rows > 0 else 20
    cell_size = min(cell_width, cell_height, 50)  #Dimensione cella max
    cell_size = max(cell_size, 10)  # min dimensione cella
    
    total_maze_width = cols * cell_size
    total_maze_height = rows * cell_size
    start_x = (maze_width - total_maze_width) // 2
    start_y = 20

    maze_area = pygame.Rect(10, 10, maze_width - 20, window_height - 120)
    pygame.draw.rect(screen, (255, 255, 255), maze_area)
    pygame.draw.rect(screen, (150, 150, 150), maze_area, 2)
    
    for i in range(rows):
        for j in range(cols):
            x = start_x + j * cell_size
            y = start_y + i * cell_size
            
            cell_value = maze[i][j]
            color = COLORS.get(cell_value, (128, 128, 128))  # 
            
            
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            
            
            pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1)
    
    return cell_size, start_y + total_maze_height

def draw_legend(screen, maze_end_y, maze, window_height):
    """Disegna la legenda dei colori"""
    font = pygame.font.Font(None, 18)
    legend_y = max(maze_end_y + 20, window_height - 80)  
    
    present_cells = set()
    for row in maze:
        for cell in row:
            present_cells.add(cell)
    
    x_offset = 20
    cells_per_row = max(1, (len(present_cells) + 1) // 2)  
    col_count = 0
    
    for cell_type in sorted(present_cells):
        if cell_type in COLORS:
            # Disegna quadratino colorato
            pygame.draw.rect(screen, COLORS[cell_type], (x_offset, legend_y, 12, 12))
            pygame.draw.rect(screen, (0, 0, 0), (x_offset, legend_y, 12, 12), 1)
            
            # Disegna testo
            text = font.render(f"{cell_type}: {CELL_NAMES[cell_type]}", True, (0, 0, 0))
            screen.blit(text, (x_offset + 17, legend_y - 1))
            
            col_count += 1
            x_offset += 120
            
            if col_count >= cells_per_row and legend_y < window_height - 40:
                x_offset = 20
                legend_y += 18

def main():

    # Chiedi il nome del file
    filename = input("Inserisci il nome del labirinto (l3.txt, 31*31) ").strip()
    if not filename:
        filename = "l3.txt"

           
    # Carica il labirinto
    maze = load_maze_from_file(filename)
    
    if not maze or len(maze) == 0:
        print("Impossibile caricare il labirinto. Uscita.")
        return
    
    print(f"Labirinto caricato: {len(maze)}x{len(maze[0])}")
    
    # Calcola dimensioni finestra iniziali
    rows, cols = len(maze), len(maze[0]) if maze else 0
    maze_width = max(500, min(800, cols * 35))  
    window_width = maze_width + BUTTON_PANEL_WIDTH + 30
    window_height = max(WINDOW_SIZE, 500)
    
    # Crea finestra ridimensionabile
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption(f"Labirinto da {filename} - Ridimensionabile")
    
    # Variabili per il ridimensionamento dinamico
    current_width = window_width
    current_height = window_height
    
    # Crea i pulsanti 3x3 iniziali
    def update_button_positions():
        global buttons
        maze_area_width = current_width - BUTTON_PANEL_WIDTH - 30
        panel_center_x = maze_area_width + (BUTTON_PANEL_WIDTH // 2)
        button_grid_width = 3 * 120 + 2 * 15 
        button_start_x = panel_center_x - (button_grid_width // 2)
        button_start_y = 100
        buttons = create_button_grid(button_start_x, button_start_y)
    
    update_button_positions()
    
    # Loop principale
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Gestisce il ridimensionamento della finestra
                current_width, current_height = event.w, event.h
                # Imposta dimensioni minime
                current_width = max(current_width, 600)
                current_height = max(current_height, 400)
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                update_button_positions()  # Riposiziona i pulsanti
                print(f"Finestra ridimensionata: {current_width}x{current_height}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    new_maze = load_maze_from_file(filename)
                    if new_maze:
                        maze = new_maze
                        print("Labirinto ricaricato!")
                    else:
                        print("Errore nel ricaricamento!")
                
            
                          
            for i, button in enumerate(buttons):
                result = button.handle_event(event)
                if result == "clicked":
                    maze = handle_button_click(i + 1, maze, screen, current_width, current_height, buttons) 
        
        # Sfondo generale
        screen.fill((200, 200, 200))
        
        # Calcola larghezza area labirinto dinamicamente
        maze_area_width = current_width - BUTTON_PANEL_WIDTH - 30
        
        # Disegna tutto solo se maze è valido
        if maze:
            cell_size, maze_end_y = draw_maze(screen, maze, maze_area_width, current_height)
            draw_legend(screen, maze_end_y, maze, current_height)
        
        # Disegna il pannello dei pulsanti separato
        draw_button_panel(screen, maze_area_width, current_height, buttons)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def handle_button_click(button_number, maze, screen, current_width, current_height,buttons):

    """Gestisce il click su un pulsante"""

    print(f"Pulsante {button_number} premuto!")
    def draw_step(current):
        maze_copy = [row.copy() for row in maze]
        i, j = current
        if maze_copy[i][j] not in (2, 3):
            maze_copy[i][j] = 10  
        draw_maze(screen, maze_copy, current_width - BUTTON_PANEL_WIDTH - 30, current_height)
        draw_legend(screen, 0, maze_copy, current_height)
        draw_button_panel(screen, current_width - BUTTON_PANEL_WIDTH - 30, current_height, buttons)

    
    if button_number == 1:
        print("Algoritmo A*")
        start_time = time.time()
        from Astar import AStarSolver

        solver = AStarSolver(maze)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()
        print("\nPercorso ottimo (A*):")
        for pos in path:
            print(pos)

        print("\nCosto totale (A*):", solver.get_path_cost())

        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
    elif button_number == 2:
        print("Algoritmo  Simulated Annealing")
        start_time = time.time()

        from SimulatedAnnealing import SimulatedAnnealingSolver

        solver = SimulatedAnnealingSolver(maze)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()
        print("\nPercorso ottimo (A*):")
        for pos in path:
            print(pos)

        print("\nCosto totale (A*):", solver.get_path_cost())

        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
    elif button_number == 3:
        from ucs import UniformCostSolver
        print("Algoritmo  a costo uniforme")
        start_time = time.time()

        solver = UniformCostSolver(maze)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()


        print("\nPercorso ottimo (UCS):")
        for pos in path:
            print(pos)

        print("\nCosto totale (UCS):", solver.get_path_cost())

        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
    elif button_number == 4:
        print("Algoritmo  Greedy")
        start_time = time.time()
        from Greedy import GreedySolver
        
        solver = GreedySolver(maze)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        
        maze[:] = solver.get_maze_with_path()
        print("Greedy:")
        for pos in path:
            print(pos)

        print("Greedy:", solver.get_path_cost())
        
        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
        
    elif button_number == 5:
        print("Algoritmo  Hill Climbing")
        start_time = time.time()
        from HillClimbing import HillClimbingSolver
        
        solver = HillClimbingSolver(maze)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
       
        maze[:] = solver.get_maze_with_path()
        print("Hill Climbing:")
        for pos in path:
            print(pos)

        print("Hill Climbing:", solver.get_path_cost())
        
        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
        
    elif button_number == 6:
        print("Algoritmo  Depth-Limited Search")
        start_time = time.time()
        from DLS import DLSSolver
        
        solver = DLSSolver(maze)
        #il parametro 'limit' del metodo solver.solve assegnato a path è modificabile per impostare il limite della ricerca in profondità
        path = solver.solve(limit=50, step_mode=True, screen=screen, draw_func=draw_step)
        
        maze[:] = solver.get_maze_with_path()
        print("DLS:")
        for pos in path:
            print(pos)

        print("DLS:", solver.get_path_cost())         
        
        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
        

    elif button_number == 7:
        print("Algoritmo  Local beam")
        start_time = time.time()
        from LocalBeam import LocalBeamSolver
        solver = LocalBeamSolver(maze, beam_width = 15)
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()


        print("Soluzione local beam:")
        for pos in path:
            print(pos)


        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')

    elif button_number == 8:
        print("Algoritmo  in ampiezza")
        start_time = time.time()
        from Ampiezza import BreadthFirstSolver

        solver = BreadthFirstSolver(maze)
        
        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()


        print("\n Soluzone ottima, ricerca in ampiezza")
        for pos in path:
            print(pos)


        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')


    elif button_number == 9:
        print("Algoritmo  Genetico")
        start_time = time.time()
        from Genetici import GeneticMazeSolver
        solver = GeneticMazeSolver(maze, 30, 50, 0.1)
        path = solver.solve()

        if path:
            maze_with_path = solver.get_maze_with_path()
            return maze_with_path
        else:
            print("Nessun percorso trovato") 

        path = solver.solve(step_mode=True, screen=screen, draw_func=draw_step)
        maze[:] = solver.get_maze_with_path()


        print("\n Soluzone ottima, ricerca in ampiezza")
        for pos in path:
            print(pos)

        end_time = time.time()
        tot_time = end_time-start_time
        print(f'Tempo trascorso: {tot_time}')
    return maze

if __name__ == "__main__":
    main()