from maze3d import generate_maze, solve_maze, adjust_3d_maze
from schematics import maze_to_schematic, save_schematic

if __name__ == "__main__":
    # Original maze dimensions
    dim_x, dim_y, dim_z = 21, 21, 21

    # Generate the maze
    maze = generate_maze(dim_x, dim_y, dim_z)

    # Define the start and end points
    start = (1, 1, 1)
    end = (dim_x - 2, dim_y - 2, dim_z - 2)

    # Solve the maze to get the path
    paths = solve_maze(maze, start, end)

    # Adjust the maze, path, and start/end for spacing
    maze, paths, new_start, new_end = adjust_3d_maze(maze, paths)

    # Save the maze as a schematic
    folder = "C:\\Users\\nikit\\curseforge\\minecraft\\Instances\\Lm\\schematics"
    filename = "3dmaze"
    schematic = maze_to_schematic(maze, paths, wall_block_id="minecraft:glass", floor_block_id="minecraft:air")
    save_schematic(schematic, folder, filename)

    print(f"Schematic saved as {filename}")
