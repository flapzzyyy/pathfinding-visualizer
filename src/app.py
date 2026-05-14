import time
from flask import Flask, render_template_string, request, jsonify

# Local
# from algorithm import Pathfinder
# from map import MapManager
# from ui import get_html

# Deploy
from src.algorithm import Pathfinder
from src.map import MapManager
from src.ui import get_html

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

finder = Pathfinder()

@app.route('/')
def index():
    return render_template_string(get_html())


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    matrix = data.get('matrix')
    algo_key = data.get('algorithm', 'bfs')

    if not matrix:
        return jsonify({'error': 'No matrix provided'}), 400

    temp_map = MapManager(len(matrix), len(matrix[0]))
    temp_map.matrix = matrix
    
    ok, err = temp_map.validate()
    if not ok:
        return jsonify({'error': err}), 400

    if not hasattr(finder, algo_key):
        return jsonify({'error': f'Unknown algorithm: {algo_key}'}), 400
    
    algo_func = getattr(finder, algo_key)

    start = temp_map.find_cell(MapManager.START)
    end = temp_map.find_cell(MapManager.END)

    t0 = time.perf_counter()
    path, visited_order = algo_func(matrix, start, end)
    elapsed = time.perf_counter() - t0

    algo_names = {
        'bfs': 'Breadth-First Search',
        'dfs': 'Depth-First Search',
        'dijkstra': "Dijkstra's Algorithm",
        'astar': 'A* Search',
        'greedy_best_first': 'Greedy Best-First Search'
    }

    return jsonify({
        'path': path,
        'visited_order': visited_order,
        'path_length': len(path) - 1 if path else 0,
        'visited_count': len(visited_order),
        'time_ms': round(elapsed * 1000, 3),
        'algo_short': algo_key.upper(),
        'algo_full': algo_names.get(algo_key, algo_key),
        'found': path is not None,
        'start': list(start),
        'end': list(end),
    })

# Local
# if __name__ == '__main__':
#     print("Pathfinding Visualizer")
#     print("Local: http://localhost:5000")
#     app.run(debug=True, host='0.0.0.0', port=5000)
