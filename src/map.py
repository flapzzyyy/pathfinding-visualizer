class MapManager:
    """
    Manages the matrix state, cell types, and validation.
    """

    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.matrix = self.make_empty_matrix(rows, cols)

    def make_empty_matrix(self, rows, cols):
        return [[self.EMPTY] * cols for _ in range(rows)]

    def find_cell(self, value):
        for r, row in enumerate(self.matrix):
            for c, cell in enumerate(row):
                if cell == value:
                    return (r, c)
        return None

    def validate(self):
        if not self.matrix or not self.matrix[0]:
            return False, 'Matrix is empty.'
        
        start = self.find_cell(self.START)
        end = self.find_cell(self.END)
        
        if start is None:
            return False, 'No start cell defined.'
        if end is None:
            return False, 'No end (finish) cell defined.'
        
        return True, None

    def set_cell(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        if value in (self.START, self.END):
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.matrix[r][c] == value:
                        self.matrix[r][c] = self.EMPTY
        
        self.matrix[row][col] = value

    def get_start_end(self):
        return self.find_cell(self.START), self.find_cell(self.END)