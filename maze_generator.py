import random

import numpy as np
from collections import deque


def create_empty_maze(dim_x, dim_y, dim_z):
    """
    Create an empty 3D maze filled with walls.
    """
    return [[[1 for _ in range(dim_z)] for _ in range(dim_y)] for _ in range(dim_x)]

def is_valid_move(x, y, z, dim_x, dim_y, dim_z):
    """
    Check if a move is within bounds of the maze.
    """
    return 0 <= x < dim_x and 0 <= y < dim_y and 0 <= z < dim_z

def get_neighbors(x, y, z, dim_x, dim_y, dim_z):
    """
    Return a list of neighboring cells with their directions.
    """
    directions = [
        (2, 0, 0), (-2, 0, 0),  # Along X-axis
        (0, 2, 0), (0, -2, 0),  # Along Y-axis
        (0, 0, 2), (0, 0, -2),  # Along Z-axis
    ]
    neighbors = []
    for dx, dy, dz in directions:
        nx, ny, nz = x + dx, y + dy, z + dz
        if is_valid_move(nx, ny, nz, dim_x, dim_y, dim_z):
            neighbors.append((nx, ny, nz, dx // 2, dy // 2, dz // 2))
    return neighbors

def generate_maze(dim_x, dim_y, dim_z):
    """
    Generate a 3D maze using the recursive backtracking algorithm.
    """
    maze = create_empty_maze(dim_x, dim_y, dim_z)

    # Start at a random cell
    start_x, start_y, start_z = random.randrange(1, dim_x, 2), random.randrange(1, dim_y, 2), random.randrange(1, dim_z, 2)
    maze[start_x][start_y][start_z] = 0

    # Stack for backtracking
    stack = [(start_x, start_y, start_z)]

    while stack:
        x, y, z = stack[-1]
        neighbors = get_neighbors(x, y, z, dim_x, dim_y, dim_z)
        random.shuffle(neighbors)  # Shuffle neighbors for randomness

        for nx, ny, nz, dx, dy, dz in neighbors:
            if maze[nx][ny][nz] == 1:  # If the neighbor is a wall
                # Break the wall between the current cell and the neighbor
                maze[x + dx][y + dy][z + dz] = 0
                maze[nx][ny][nz] = 0
                stack.append((nx, ny, nz))
                break
        else:
            stack.pop()

    return maze

def adjust_3d_maze(maze, solutions=None, start=None, end=None):
    """
    Adjusts a 3D maze by ensuring proper distance between walls in all dimensions.
    Also updates solutions, start, and end positions dynamically.

    Args:
        maze (np.array): A 3D maze where 1 represents walls and 0 represents paths.
        solutions (list of list of tuples): Solution paths to adjust.
        start (tuple): The start position in the maze (x, y, z).
        end (tuple): The end position in the maze (x, y, z).

    Returns:
        tuple: (new_maze, new_solutions, new_start, new_end)
            - new_maze: The adjusted 3D maze.
            - new_solutions: The updated solution paths.
            - new_start: The updated start position.
            - new_end: The updated end position.
    """
    def fix_disconnected_walls(maze, axis, idx):
        """Fix walls disconnected by a newly inserted slice in a specific axis."""
        if axis == 0:  # Fixing along X-axis (depth)
            for y in range(maze.shape[1]):
                for z in range(maze.shape[2]):
                    if maze[idx, y, z] == 0 and maze[idx - 1, y, z] == 1 and maze[idx + 1, y, z] == 1:
                        maze[idx, y, z] = 1
        elif axis == 1:  # Fixing along Y-axis (rows)
            for x in range(maze.shape[0]):
                for z in range(maze.shape[2]):
                    if maze[x, idx, z] == 0 and maze[x, idx - 1, z] == 1 and maze[x, idx + 1, z] == 1:
                        maze[x, idx, z] = 1
        elif axis == 2:  # Fixing along Z-axis (columns)
            for x in range(maze.shape[0]):
                for y in range(maze.shape[1]):
                    if maze[x, y, idx] == 0 and maze[x, y, idx - 1] == 1 and maze[x, y, idx + 1] == 1:
                        maze[x, y, idx] = 1

    # Initialize variables
    maze = np.array(maze.copy())
    depth, rows, cols = maze.shape
    if solutions is None:
        solutions = []
    new_solutions = []
    if start is None:
        start = (0, 0, 0)
    if end is None:
        end = (depth - 1, rows - 1, cols - 1)

    # Convert solutions, start, and end into mutable lists of coordinates
    solution_coordinates = [
        [[x, y, z] for x, y, z in solution]
        for solution in solutions
    ]
    mutable_start = list(start)
    mutable_end = list(end)

    # Adjust the maze structure
    x = 0
    while x < depth:
        y = 0
        while y < rows:
            z = 0
            while z < cols:
                if maze[x, y, z] == 0:
                    # Check spacing along Z (columns)
                    if z > 0 and z < cols - 1 and maze[x, y, z - 1] == 1 and maze[x, y, z + 1] == 1:
                        maze = np.insert(maze, z + 1, 0, axis=2)
                        cols += 1
                        fix_disconnected_walls(maze, axis=2, idx=z + 1)

                        # Update all relevant coordinates after column insertion
                        for solution in solution_coordinates:
                            for coord in solution:
                                if coord[2] >= z + 1:
                                    coord[2] += 1
                        if mutable_start[2] >= z + 1:
                            mutable_start[2] += 1
                        if mutable_end[2] >= z + 1:
                            mutable_end[2] += 1

                    # Check spacing along Y (rows)
                    if y > 0 and y < rows - 1 and maze[x, y - 1, z] == 1 and maze[x, y + 1, z] == 1:
                        maze = np.insert(maze, y + 1, 0, axis=1)
                        rows += 1
                        fix_disconnected_walls(maze, axis=1, idx=y + 1)

                        # Update all relevant coordinates after row insertion
                        for solution in solution_coordinates:
                            for coord in solution:
                                if coord[1] >= y + 1:
                                    coord[1] += 1
                        if mutable_start[1] >= y + 1:
                            mutable_start[1] += 1
                        if mutable_end[1] >= y + 1:
                            mutable_end[1] += 1

                    # Check spacing along X (depth)
                    if x > 0 and x < depth - 1 and maze[x - 1, y, z] == 1 and maze[x + 1, y, z] == 1:
                        maze = np.insert(maze, x + 1, 0, axis=0)
                        depth += 1
                        fix_disconnected_walls(maze, axis=0, idx=x + 1)

                        # Update all relevant coordinates after depth insertion
                        for solution in solution_coordinates:
                            for coord in solution:
                                if coord[0] >= x + 1:
                                    coord[0] += 1
                        if mutable_start[0] >= x + 1:
                            mutable_start[0] += 1
                        if mutable_end[0] >= x + 1:
                            mutable_end[0] += 1
                z += 1
            y += 1
        x += 1

    # Convert updated solution coordinates back to tuples
    new_solutions = [
        [(x, y, z) for x, y, z in solution]
        for solution in solution_coordinates
    ]

    # Convert mutable start and end back to tuples
    new_start = tuple(mutable_start)
    new_end = tuple(mutable_end)

    return maze, new_solutions, new_start, new_end


def solve_maze(maze, start, end):
    """
    Solve the 3D maze using breadth-first search and return the shortest path.
    """
    dim_x = len(maze)
    dim_y = len(maze[0])
    dim_z = len(maze[0][0])

    # Initialize BFS queue and visited set
    queue = deque([(start, [start])])  # each item in the queue is a tuple (position, path)
    visited = set([start])

    # Possible moves (x, y, z directions)
    directions = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

    while queue:
        (x, y, z), current_path = queue.popleft()

        # Check if we've reached the end
        if (x, y, z) == end:
            return [current_path]

        # Explore the neighbors
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if is_valid_move(nx, ny, nz, dim_x, dim_y, dim_z) and maze[nx][ny][nz] == 0 and (nx, ny, nz) not in visited:
                visited.add((nx, ny, nz))
                queue.append(((nx, ny, nz), current_path + [(nx, ny, nz)]))

    return [[]]  # Return an empty list if no path is found

# def visualize_3d_maze(maze, path=None):
#     """
#     Visualize the 3D maze using matplotlib.
#     """
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#
#     dim_x = len(maze)
#     dim_y = len(maze[0])
#     dim_z = len(maze[0][0])
#
#     # Plot each cell in the maze
#     for x in range(dim_x):
#         for y in range(dim_y):
#             for z in range(dim_z):
#                 if maze[x][y][z] == 1:  # Wall
#                     ax.bar3d(x, y, z, 1, 1, 1, color="black", alpha=0.05)
#
#     # Highlight the solving path
#     if path:
#         px, py, pz = zip(*path)
#         ax.plot(px, py, pz, color="red", linewidth=2, label="Solution Path")
#
#     ax.set_xlabel("X Axis")
#     ax.set_ylabel("Y Axis")
#     ax.set_zlabel("Z Axis")
#     plt.legend()
#     plt.show()

def print_3d_maze(maze):
    """
    Print the 3D maze layer by layer.
    """
    dim_x = len(maze)
    dim_y = len(maze[0])
    dim_z = len(maze[0][0])

    for z in range(dim_z):
        print(f"Level {z}:\n")
        for y in range(dim_y):
            row = ""
            for x in range(dim_x):
                row += "  " if maze[x][y][z] == 0 else "##"
            print(row)
        print("\n")