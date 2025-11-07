"""
Jeu de Bataille Navale (Battleship Game)
Un jeu complet avec interface graphique tkinter
"""

import tkinter as tk
from tkinter import messagebox
import random


class Ship:
    """Représente un navire dans le jeu"""
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = set()
    
    def is_sunk(self):
        """Vérifie si le navire est coulé"""
        return len(self.hits) == self.size


class Board:
    """Représente une grille de jeu"""
    def __init__(self, size=10):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = []
    
    def is_valid_position(self, row, col, size, horizontal):
        """Vérifie si une position est valide pour placer un navire"""
        if horizontal:
            if col + size > self.size:
                return False
            for c in range(col, col + size):
                if self.grid[row][c] != '~':
                    return False
                # Vérifier les cases adjacentes
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r, c_check = row + dr, c + dc
                        if 0 <= r < self.size and 0 <= c_check < self.size:
                            if self.grid[r][c_check] == 'S':
                                return False
        else:
            if row + size > self.size:
                return False
            for r in range(row, row + size):
                if self.grid[r][col] != '~':
                    return False
                # Vérifier les cases adjacentes
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r_check, c = r + dr, col + dc
                        if 0 <= r_check < self.size and 0 <= c < self.size:
                            if self.grid[r_check][c] == 'S':
                                return False
        return True
    
    def place_ship(self, ship, row, col, horizontal):
        """Place un navire sur la grille"""
        if not self.is_valid_position(row, col, ship.size, horizontal):
            return False
        
        positions = []
        if horizontal:
            for c in range(col, col + ship.size):
                self.grid[row][c] = 'S'
                positions.append((row, c))
        else:
            for r in range(row, row + ship.size):
                self.grid[r][col] = 'S'
                positions.append((r, col))
        
        ship.positions = positions
        self.ships.append(ship)
        return True
    
    def place_ships_randomly(self, ship_sizes):
        """Place tous les navires aléatoirement"""
        for name, size in ship_sizes:
            ship = Ship(name, size)
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                horizontal = random.choice([True, False])
                placed = self.place_ship(ship, row, col, horizontal)
                attempts += 1
            if not placed:
                return False
        return True
    
    def receive_attack(self, row, col):
        """Reçoit une attaque et retourne le résultat"""
        if self.grid[row][col] == '~':
            self.grid[row][col] = 'O'  # Raté
            return 'miss'
        elif self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'  # Touché
            # Trouver le navire touché
            for ship in self.ships:
                if (row, col) in ship.positions:
                    ship.hits.add((row, col))
                    if ship.is_sunk():
                        return f'sunk:{ship.name}'
                    return 'hit'
        return 'already_hit'
    
    def all_ships_sunk(self):
        """Vérifie si tous les navires sont coulés"""
        return all(ship.is_sunk() for ship in self.ships)


class BattleshipGame:
    """Interface graphique du jeu de bataille navale"""
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.root.resizable(False, False)
        
        # Configuration du jeu
        self.board_size = 10
        self.cell_size = 40
        self.ship_sizes = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Contre-torpilleur", 3),
            ("Sous-marin", 3),
            ("Torpilleur", 2)
        ]
        
        # Initialisation des grilles
        self.player_board = Board(self.board_size)
        self.computer_board = Board(self.board_size)
        
        # État du jeu
        self.game_started = False
        self.player_turn = True
        self.placing_ships = True
        self.current_ship_index = 0
        self.ship_horizontal = True
        
        # Interface
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(padx=20, pady=20)
        
        # Titre
        title = tk.Label(main_frame, text="🚢 BATAILLE NAVALE 🚢", 
                        font=('Arial', 24, 'bold'), bg='#2C3E50', fg='white')
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Instructions
        self.info_label = tk.Label(main_frame, 
                                   text="Placez vos navires (Clic pour placer, R pour rotation)",
                                   font=('Arial', 12), bg='#2C3E50', fg='white')
        self.info_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Frame pour les grilles
        boards_frame = tk.Frame(main_frame, bg='#2C3E50')
        boards_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Grille du joueur
        player_frame = tk.LabelFrame(boards_frame, text="Votre Flotte", 
                                     font=('Arial', 14, 'bold'), bg='#34495E', fg='white')
        player_frame.grid(row=0, column=0, padx=10)
        
        self.player_canvas = tk.Canvas(player_frame, width=self.board_size*self.cell_size,
                                       height=self.board_size*self.cell_size, bg='#3498DB')
        self.player_canvas.pack(padx=5, pady=5)
        self.player_canvas.bind('<Button-1>', self.on_player_board_click)
        
        # Grille de l'ordinateur
        computer_frame = tk.LabelFrame(boards_frame, text="Flotte Ennemie", 
                                      font=('Arial', 14, 'bold'), bg='#34495E', fg='white')
        computer_frame.grid(row=0, column=1, padx=10)
        
        self.computer_canvas = tk.Canvas(computer_frame, width=self.board_size*self.cell_size,
                                        height=self.board_size*self.cell_size, bg='#3498DB')
        self.computer_canvas.pack(padx=5, pady=5)
        self.computer_canvas.bind('<Button-1>', self.on_computer_board_click)
        
        # Boutons de contrôle
        control_frame = tk.Frame(main_frame, bg='#2C3E50')
        control_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.rotate_button = tk.Button(control_frame, text="Rotation (R)", 
                                      command=self.toggle_ship_orientation,
                                      font=('Arial', 12), bg='#E74C3C', fg='white',
                                      padx=10, pady=5)
        self.rotate_button.pack(side=tk.LEFT, padx=5)
        
        self.start_button = tk.Button(control_frame, text="Placement Aléatoire", 
                                     command=self.random_placement,
                                     font=('Arial', 12), bg='#27AE60', fg='white',
                                     padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.new_game_button = tk.Button(control_frame, text="Nouvelle Partie", 
                                        command=self.new_game,
                                        font=('Arial', 12), bg='#9B59B6', fg='white',
                                        padx=10, pady=5)
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Bind keyboard
        self.root.bind('r', lambda e: self.toggle_ship_orientation())
        self.root.bind('R', lambda e: self.toggle_ship_orientation())
        
        # Dessiner les grilles
        self.draw_boards()
        
    def draw_boards(self):
        """Dessine les deux grilles"""
        # Grille du joueur
        self.player_canvas.delete('all')
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.player_board.grid[row][col]
                color = self.get_cell_color(cell, True)
                
                self.player_canvas.create_rectangle(x1, y1, x2, y2, 
                                                   fill=color, outline='#2C3E50', width=2)
                
                # Afficher les symboles
                if cell in ['X', 'O']:
                    self.draw_symbol(self.player_canvas, x1, y1, cell)
        
        # Grille de l'ordinateur
        self.computer_canvas.delete('all')
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.computer_board.grid[row][col]
                # Ne pas montrer les navires de l'ordinateur
                if cell == 'S' and self.game_started:
                    color = '#3498DB'
                else:
                    color = self.get_cell_color(cell, False)
                
                self.computer_canvas.create_rectangle(x1, y1, x2, y2, 
                                                     fill=color, outline='#2C3E50', width=2)
                
                # Afficher les symboles
                if cell in ['X', 'O']:
                    self.draw_symbol(self.computer_canvas, x1, y1, cell)
    
    def get_cell_color(self, cell, is_player):
        """Retourne la couleur d'une cellule"""
        if cell == '~':
            return '#3498DB'  # Eau
        elif cell == 'S':
            return '#95A5A6' if is_player else '#3498DB'  # Navire
        elif cell == 'X':
            return '#E74C3C'  # Touché
        elif cell == 'O':
            return '#ECF0F1'  # Raté
        return '#3498DB'
    
    def draw_symbol(self, canvas, x, y, symbol):
        """Dessine un symbole (X ou O) dans une cellule"""
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        
        if symbol == 'X':
            # Croix rouge
            canvas.create_line(x+10, y+10, x+self.cell_size-10, y+self.cell_size-10,
                             fill='#C0392B', width=4)
            canvas.create_line(x+self.cell_size-10, y+10, x+10, y+self.cell_size-10,
                             fill='#C0392B', width=4)
        elif symbol == 'O':
            # Cercle blanc
            canvas.create_oval(x+10, y+10, x+self.cell_size-10, y+self.cell_size-10,
                             outline='#7F8C8D', width=3, fill='')
    
    def on_player_board_click(self, event):
        """Gère les clics sur la grille du joueur (placement de navires)"""
        if not self.placing_ships or self.game_started:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if row >= self.board_size or col >= self.board_size:
            return
        
        if self.current_ship_index < len(self.ship_sizes):
            name, size = self.ship_sizes[self.current_ship_index]
            ship = Ship(name, size)
            
            if self.player_board.place_ship(ship, row, col, self.ship_horizontal):
                self.current_ship_index += 1
                
                if self.current_ship_index >= len(self.ship_sizes):
                    self.placing_ships = False
                    self.start_game()
                else:
                    next_ship = self.ship_sizes[self.current_ship_index]
                    self.info_label.config(text=f"Placez: {next_ship[0]} (taille {next_ship[1]})")
                
                self.draw_boards()
    
    def on_computer_board_click(self, event):
        """Gère les clics sur la grille de l'ordinateur (attaques)"""
        if not self.game_started or not self.player_turn:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if row >= self.board_size or col >= self.board_size:
            return
        
        # Vérifier si la case a déjà été attaquée
        if self.computer_board.grid[row][col] in ['X', 'O']:
            self.info_label.config(text="Case déjà attaquée!")
            return
        
        self.player_attack(row, col)
    
    def player_attack(self, row, col):
        """Le joueur attaque"""
        result = self.computer_board.receive_attack(row, col)
        
        if result == 'miss':
            self.info_label.config(text="Raté!")
        elif result == 'hit':
            self.info_label.config(text="Touché!")
        elif result.startswith('sunk'):
            ship_name = result.split(':')[1]
            self.info_label.config(text=f"Coulé! {ship_name}")
        
        self.draw_boards()
        
        if self.computer_board.all_ships_sunk():
            messagebox.showinfo("Victoire!", "Vous avez gagné! 🎉")
            self.game_started = False
            return
        
        if result == 'miss':
            self.player_turn = False
            self.root.after(1000, self.computer_turn)
    
    def computer_turn(self):
        """Tour de l'ordinateur"""
        if not self.game_started:
            return
        
        self.info_label.config(text="L'ordinateur réfléchit...")
        self.root.update()
        
        # IA simple: attaque aléatoire
        attempts = 0
        while attempts < 100:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            
            if self.player_board.grid[row][col] not in ['X', 'O']:
                break
            attempts += 1
        
        result = self.player_board.receive_attack(row, col)
        
        if result == 'miss':
            self.info_label.config(text=f"L'ordinateur a raté en ({row}, {col})")
        elif result == 'hit':
            self.info_label.config(text=f"L'ordinateur a touché en ({row}, {col})!")
        elif result.startswith('sunk'):
            ship_name = result.split(':')[1]
            self.info_label.config(text=f"L'ordinateur a coulé votre {ship_name}!")
        
        self.draw_boards()
        
        if self.player_board.all_ships_sunk():
            messagebox.showinfo("Défaite", "L'ordinateur a gagné!")
            self.game_started = False
            return
        
        if result == 'miss':
            self.player_turn = True
            self.info_label.config(text="À votre tour!")
        else:
            # L'ordinateur rejoue s'il touche
            self.root.after(1000, self.computer_turn)
    
    def toggle_ship_orientation(self):
        """Change l'orientation du navire à placer"""
        if self.placing_ships and not self.game_started:
            self.ship_horizontal = not self.ship_horizontal
            orientation = "Horizontale" if self.ship_horizontal else "Verticale"
            current_ship = self.ship_sizes[self.current_ship_index] if self.current_ship_index < len(self.ship_sizes) else None
            if current_ship:
                self.info_label.config(text=f"Placez: {current_ship[0]} - {orientation}")
    
    def random_placement(self):
        """Place les navires aléatoirement"""
        if self.game_started:
            return
        
        # Réinitialiser la grille
        self.player_board = Board(self.board_size)
        self.player_board.place_ships_randomly(self.ship_sizes)
        self.current_ship_index = len(self.ship_sizes)
        self.placing_ships = False
        self.draw_boards()
        self.start_game()
    
    def start_game(self):
        """Démarre le jeu"""
        # Placer les navires de l'ordinateur
        self.computer_board.place_ships_randomly(self.ship_sizes)
        self.game_started = True
        self.player_turn = True
        self.info_label.config(text="À votre tour! Cliquez sur la grille ennemie pour attaquer.")
        self.rotate_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.draw_boards()
    
    def new_game(self):
        """Commence une nouvelle partie"""
        self.player_board = Board(self.board_size)
        self.computer_board = Board(self.board_size)
        self.game_started = False
        self.player_turn = True
        self.placing_ships = True
        self.current_ship_index = 0
        self.ship_horizontal = True
        self.rotate_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.info_label.config(text="Placez vos navires (Clic pour placer, R pour rotation)")
        self.draw_boards()


def main():
    """Fonction principale"""
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
