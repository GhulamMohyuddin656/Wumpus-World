from flask import Flask, render_template, request, jsonify
from wumpusworld import WumpusWorld
from wumpusagent import WumpusAgent

app = Flask(__name__)

# Global state to hold our game
game_state = {
    "world": None,
    "agent": None,
    "rover_r": 0,
    "rover_c": 0,
    "direction": "right",
    "status": "playing", # playing, dead, won
    "size": 4
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    size = game_state["size"]
    game_state["world"] = WumpusWorld(size, size)
    game_state["agent"] = WumpusAgent(size, size)
    game_state["rover_r"] = 0
    game_state["rover_c"] = 0
    game_state["direction"] = "right"
    game_state["status"] = "playing"
    
    # Prove 0,0 is safe
    game_state["agent"].tell("p", 0, 0, False)
    game_state["agent"].tell("w", 0, 0, False)
    game_state["agent"].visited.add((0,0))
    
    return process_turn()

@app.route('/move', methods=['POST'])
def move():
    if game_state["status"] != "playing":
        return process_turn()

    direction = request.json.get('direction')
    game_state["direction"] = direction
    r, c = game_state["rover_r"], game_state["rover_c"]
    
    if direction == "up" and r > 0: r -= 1
    elif direction == "down" and r < game_state["size"] - 1: r += 1
    elif direction == "left" and c > 0: c -= 1
    elif direction == "right" and c < game_state["size"] - 1: c += 1
    
    game_state["rover_r"] = r
    game_state["rover_c"] = c
    game_state["agent"].visited.add((r, c))
    
    return process_turn()

def process_turn():
    world = game_state["world"]
    agent = game_state["agent"]
    r, c = game_state["rover_r"], game_state["rover_c"]
    
    # 1. Did we die or win?
    cell = world.grid[r][c]
    if cell["p"] or cell["w"]:
        game_state["status"] = "dead"
    elif cell["g"]:
        game_state["status"] = "won"
        
    # 2. Get Percepts and Update Agent Notebook
    percepts = world.get_percepts(r, c)
    agent.tell('b', r, c, percepts["breeze"])
    agent.tell('s', r, c, percepts["stench"])
    
    # 3. Ask about neighbors
    safe_cells = list(agent.safe_known)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < world.row and 0 <= nc < world.col:
            if agent.ask_is_safe(nr, nc):
                if (nr, nc) not in safe_cells:
                    safe_cells.append((nr, nc))

    return jsonify({
        "grid_size": world.row,
        "rover_pos": [r, c],
        "direction": game_state["direction"],
        "visited": list(agent.visited),
        "safe_cells": safe_cells,
        "percepts": percepts,
        "status": game_state["status"],
        "hazards": world.grid # We only use this to reveal everything if game ends
    })

if __name__ == '__main__':
    app.run(debug=True)