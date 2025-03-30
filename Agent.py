from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Définition de la pièce et du robot
class Room:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]  # 0 = propre, 1 = sale
        self.robot_position = [0, 0]  # Début en haut à gauche
        self.cleaned_count = 0  # Compteur de cases nettoyées

    # Percevoir : regarder autour du robot
    def perceive(self):
        x, y = self.robot_position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Droite, Bas, Gauche, Haut
        random.shuffle(directions)  # Mélanger les directions
        possible_moves = []

        # Vérifier chaque direction
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:  # Dans les limites
                possible_moves.append([new_x, new_y])
                break  # Prendre le premier mouvement valide
        
        return possible_moves

    # Réagir : bouger et nettoyer
    def react(self, possible_moves):
        if possible_moves:  # S'il y a un mouvement possible
            new_x, new_y = possible_moves[0]  # Prendre le premier
            self.robot_position = [new_x, new_y]
            
            # Nettoyer si sale
            if self.grid[new_y][new_x] == 1:
                self.grid[new_y][new_x] = 0
                self.cleaned_count += 1

room = Room()

@app.route("/simulate")
def simulate():
    moves = room.perceive()  # Percevoir l'environnement
    room.react(moves)  # Réagir au mouvement possible
    return jsonify({
        "grid": room.grid,
        "robot_position": room.robot_position,
        "cleaned_count": room.cleaned_count
    })

if __name__ == "__main__":
    app.run(debug=True)