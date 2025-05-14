import argparse
from maze_generator import generate_maze, solve_maze, adjust_3d_maze
from gui_backend import visualize_3d_maze
from schematics import maze_to_schematic, save_schematic

def main():
    parser = argparse.ArgumentParser(description="Generate a 3D maze and export it as a Minecraft schematic.")

    parser.add_argument("--dim_x", type=int, default=21, help="Maze dimension in the X axis (must be odd).")
    parser.add_argument("--dim_y", type=int, default=21, help="Maze dimension in the Y axis (must be odd).")
    parser.add_argument("--dim_z", type=int, default=21, help="Maze dimension in the Z axis (must be odd).")

    parser.add_argument("--folder", type=str, required=True, help="Path to the folder where the schematic will be saved.")
    parser.add_argument("--filename", type=str, default="3dmaze", help="Name of the schematic file (without extension).")

    parser.add_argument("--wall_block", type=str, default="minecraft:glass", help="Block ID used for walls.")
    parser.add_argument("--floor_block", type=str, default="minecraft:air", help="Block ID used for floor/empty space.")

    parser.add_argument("--visualize", action="store_true", help="Show a 3D visualization of the generated maze.")

    args = parser.parse_args()

    # Generate the maze
    maze = generate_maze(args.dim_x, args.dim_y, args.dim_z)

    # Define the start and end points
    start = (1, 1, 1)
    end = (args.dim_x - 2, args.dim_y - 2, args.dim_z - 2)

    # Solve the maze to get the path
    paths = solve_maze(maze, start, end)

    # Adjust the maze, path, and start/end for spacing
    maze, paths, new_start, new_end = adjust_3d_maze(maze, paths)

    # Convert to schematic
    schematic = maze_to_schematic(
        maze, paths,
        wall_block_id=args.wall_block,
        floor_block_id=args.floor_block
    )

    # Save to file
    save_schematic(schematic, args.folder, args.filename)

    print(f"Schematic saved to {args.folder} as {args.filename}.schematic")

    # Show visualizer if requested
    if args.visualize:
        visualize_3d_maze(maze, paths)

if __name__ == "__main__":
    main()
