# 🗺️ Pathfinding Visualizer

An interactive web-based tool for visualizing classic pathfinding algorithms on a customizable grid. Watch in real time as algorithms explore cells, find the shortest path, and report performance metrics — all in your browser.

---

## 📖 Description

Pathfinding Visualizer is a Flask-powered application that lets you draw walls, place start and end points, and run one of five pathfinding algorithms to see how each one navigates the grid differently. Each run reports the path length, number of cells visited, and execution time — making it easy to compare algorithm behavior side by side.

---

## ✨ Main Features

- **5 Pathfinding Algorithms**: each with distinct exploration strategies:
  - **BFS** (Breadth-First Search): explores layer by layer, guarantees shortest path on unweighted grids
  - **DFS** (Depth-First Search): explores as deep as possible, does not guarantee shortest path
  - **Dijkstra's Algorithm**: weighted shortest path using a priority queue
  - **A\* Search**: heuristic-driven (Manhattan distance), finds shortest path faster than Dijkstra
  - **Greedy Best-First Search**: purely heuristic, fast but does not guarantee shortest path

- **Interactive Grid**: click to place walls, move start/end nodes, and customize the map freely

- **Step-by-step Visualization**: animated playback of visited cells and the final path

- **Performance Stats**: displays path length, visited cell count, and algorithm execution time in milliseconds

- **Grid Validation**: prevents running without a defined start and end cell

- **REST API**: `/solve` endpoint accepts a matrix + algorithm key and returns full result as JSON

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, API Flask |
| Algorithms | Pure Python (`heapq`, `collections.deque`) |
| Frontend | HTML + CSS + JavaScript |
| Deployment | Vercel |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/flapzzyyy/pathfinding-visualizer.git
cd pathfinding-visualizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python src/app.py
```

Open your browser and go to: **http://localhost:5000**

### Project Structure

```
pathfinding-visualizer/
├── src/
│   ├── algorithm.py   # BFS, DFS, Dijkstra, A*, Greedy Best-First
│   ├── map.py         # Grid state management and validation
│   └── ui.py          # HTML/CSS/JS frontend
    └── app.py         # Flask app and /solve API endpoint
│            
└── README.md
```

### API Usage

Send a `POST` request to `/solve` with a JSON body:

```json
{
  "matrix": [
    [0, 0, 1, 0],
    [2, 0, 1, 0],
    [0, 0, 0, 3]
  ],
  "algorithm": "astar"
}
```

**Cell values:** `0` = empty, `1` = wall, `2` = start, `3` = end

**Available algorithm keys:** `bfs`, `dfs`, `dijkstra`, `astar`, `greedy_best_first`

**Response:**

```json
{
  "found": true,
  "path": [[1,0], [1,1], [2,1], [2,2], [2,3]],
  "path_length": 4,
  "visited_count": 7,
  "time_ms": 0.312,
  "algo_full": "A* Search"
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

© 2026 Yoseph Kevin, Mahendra Agung, Nashwa Aulia. All rights reserved.
