import heapq
from collections import deque

class Pathfinder:
    """
    Class for pathfinding algorithms
    """
    
    @staticmethod
    def _get_neighbors(matrix, row, col):
        rows, cols = len(matrix), len(matrix[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                neighbors.append((nr, nc))
        return neighbors

    @staticmethod
    def _reconstruct_path(came_from, start, end):
        path = []
        node = end
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        return path[::-1]

    @staticmethod
    def _heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def bfs(self, matrix, start, end):
        queue = deque([start])
        visited = {start}
        came_from = {start: None}
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            if node == end:
                return self._reconstruct_path(came_from, start, end), order

            for neighbor in self._get_neighbors(matrix, *node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = node
                    queue.append(neighbor)
        return None, order

    def dfs(self, matrix, start, end):
        stack = [start]
        visited = {start}
        came_from = {start: None}
        order = []

        while stack:
            node = stack.pop()
            order.append(node)

            if node == end:
                return self._reconstruct_path(came_from, start, end), order

            for neighbor in self._get_neighbors(matrix, *node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = node
                    stack.append(neighbor)
        return None, order

    def dijkstra(self, matrix, start, end):
        dist = {start: 0}
        came_from = {start: None}
        pq = [(0, start)]
        visited = set()
        order = []

        while pq:
            cost, node = heapq.heappop(pq)
            if node in visited: continue
            visited.add(node)
            order.append(node)

            if node == end:
                return self._reconstruct_path(came_from, start, end), order

            for neighbor in self._get_neighbors(matrix, *node):
                new_cost = cost + 1
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    came_from[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor))
        return None, order

    def astar(self, matrix, start, end):
        open_set = [(0 + self._heuristic(start, end), 0, start)]
        came_from = {start: None}
        g_score = {start: 0}
        visited = set()
        order = []

        while open_set:
            f, g, node = heapq.heappop(open_set)
            if node in visited: continue
            visited.add(node)
            order.append(node)

            if node == end:
                return self._reconstruct_path(came_from, start, end), order

            for neighbor in self._get_neighbors(matrix, *node):
                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self._heuristic(neighbor, end)
                    came_from[neighbor] = node
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
        return None, order

    def greedy_best_first(self, matrix, start, end):
        open_set = [(self._heuristic(start, end), start)]
        came_from = {start: None}
        visited = set()
        order = []

        while open_set:
            h, node = heapq.heappop(open_set)
            if node in visited: continue
            visited.add(node)
            order.append(node)

            if node == end:
                return self._reconstruct_path(came_from, start, end), order

            for neighbor in self._get_neighbors(matrix, *node):
                if neighbor not in visited:
                    came_from[neighbor] = node
                    heapq.heappush(open_set, (self._heuristic(neighbor, end), neighbor))
        return None, order