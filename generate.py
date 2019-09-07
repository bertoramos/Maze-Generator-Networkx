
import random
from utils import Cell, Maze

def dfs_generator(grid):
    path = []
    
    stack = []
    seen = []

    current_cell = Cell(0, 0)
    seen.append(current_cell)

    while grid.get_dim()**2 - len(seen) != 0:
        neighbors = grid.get_neighbors(current_cell.i, current_cell.j)
        
        not_visited = []
        for cell in neighbors:
            if cell not in seen:
                not_visited.append(cell)
        
        if len(not_visited) > 0:
            neighbour = random.choice(not_visited)
            stack.append(current_cell)

            path.append((current_cell, neighbour))

            current_cell = neighbour
            seen.append(current_cell)
        else:
            current_cell = stack.pop()

    maze = Maze(path)
    return maze
