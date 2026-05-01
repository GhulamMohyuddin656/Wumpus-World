# 🌍 Wumpus World AI Agent

A web-based implementation of the classic **Wumpus World** problem, powered by a custom propositional logic parser and resolution engine. This project features a fully dynamic, graphical user interface that tracks the agent's real-time inference steps, percepts, and environment mapping.

## ✨ Key Features
* **Custom Resolution Engine:** The agent navigates the grid using a Knowledge Base (KB) and proves the safety of adjacent cells using propositional logic and resolution.
* **Dynamic Grid Resizing:** Supports custom grid dimensions (e.g., 4x4, 5x8) that render perfectly on the frontend without breaking the UI.
* **Real-Time Metrics Dashboard:** Tracks the exact number of inference steps taken by the resolution algorithm and displays active percepts (Breeze, Stench) at the agent's current location.
* **Interactive Visualization:** * 🟩 **Green:** Confirmed Safe
  * ⬜ **Gray:** Unknown / Unvisited / Fog of War
  * 🟥 **Red:** Confirmed Hazard (Pit / Wumpus)

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask (RESTful routing between UI and Agent)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (DOM manipulation and Grid mapping)
* **AI Logic:** Propositional Logic, Conjunctive Normal Form (CNF), Resolution Theorem Proving

## 📂 Project Structure
```text
📦 wumpus-world
 ┣ 📂 static
 ┃ ┗ 📂 images          # Sprites for Rover, Gold, Wumpus, Pit, Fog
 ┣ 📂 templates
 ┃ ┗ 📜 index.html      # Frontend UI, Dashboard, and JS logic
 ┣ 📜 main.py           # Flask server and game state manager
 ┣ 📜 wumpusagent.py    # The AI Agent (Knowledge Base & Resolution Engine)
 ┣ 📜 wumpusworld.py    # Environment generation and percept assignment
 ┗ 📜 README.md         # Project documentation