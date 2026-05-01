from flask import Flask, render_template, request, jsonify
from wumpusworld import WumpusWorld
from wumpusagent import WumpusAgent

app = Flask(__name__)

game_state = {
    "world": None,
    "agent": None,
    "rover_r": 0,
    "rover_c": 0,
    "direction": "right",
    "status": "playing", 
    "rows": 4,
    "cols": 4
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    # Grab separate rows and cols from frontend, default to 4 if missing
    game_state["rows"] = int(request.json.get('rows', 4))
    game_state["cols"] = int(request.json.get('cols', 4))
    
    rows = game_state["rows"]
    cols = game_state["cols"]
    
    # Generate the world dynamically with custom Rows x Cols
    game_state["world"] = WumpusWorld(rows, cols)
    game_state["agent"] = WumpusAgent(rows, cols)
    game_state["rover_r"] = 0
    game_state["rover_c"] = 0
    game_state["direction"] = "right"
    game_state["status"] = "playing"
    
    game_state["agent"].tell("p", 0, 0, False)
    game_state["agent"].tell("w", 0, 0, False)
    game_state["agent"].visited.add((0,0))
    
    return process_turn()

@app.route('/move', methods=['POST'])
def move():
    if "dead" in game_state["status"] or game_state["status"] == "won":
        return process_turn()

    direction = request.json.get('direction')
    game_state["direction"] = direction
    r, c = game_state["rover_r"], game_state["rover_c"]
    
    # Use rows and cols for boundary limits
    if direction == "up" and r > 0: r -= 1
    elif direction == "down" and r < game_state["rows"] - 1: r += 1
    elif direction == "left" and c > 0: c -= 1
    elif direction == "right" and c < game_state["cols"] - 1: c += 1
    
    game_state["rover_r"] = r
    game_state["rover_c"] = c
    game_state["agent"].visited.add((r, c))
    
    return process_turn()

def process_turn():
    world = game_state["world"]
    agent = game_state["agent"]
    r, c = game_state["rover_r"], game_state["rover_c"]
    
    cell = world.grid[r][c]
    if cell["p"]: game_state["status"] = "dead_pit"
    elif cell["w"]: game_state["status"] = "dead_wumpus"
    elif cell["g"]: game_state["status"] = "won"
        
    percepts = world.get_percepts(r, c)
    agent.tell('b', r, c, percepts["breeze"])
    agent.tell('s', r, c, percepts["stench"])
    
    safe_cells = list(agent.safe_known)
    confirmed_hazards = [] 
    
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < world.row and 0 <= nc < world.col:
            if agent.ask_is_safe(nr, nc):
                if (nr, nc) not in safe_cells:
                    safe_cells.append((nr, nc))
            else:
                is_pit = agent.prove(f"p{nr}{nc}")
                is_wumpus = agent.prove(f"w{nr}{nc}")
                if is_pit or is_wumpus:
                    confirmed_hazards.append((nr, nc))

    return jsonify({
        "grid_rows": world.row,
        "grid_cols": world.col,
        "rover_pos": [r, c],
        "direction": game_state["direction"],
        "visited": list(agent.visited),
        "safe_cells": safe_cells,
        "confirmed_hazards": confirmed_hazards,
        "percepts": percepts,
        "inference_steps": agent.inference_steps,
        "status": game_state["status"],
        "hazards": world.grid 
    })

if __name__ == '__main__':
    app.run(debug=True)