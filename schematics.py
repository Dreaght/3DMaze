import mcschematic

def maze_to_schematic(maze, paths=None, wall_block_id="minecraft:stone", floor_block_id="minecraft:air"):
    """
    Convert a 3D maze to a Minecraft schematic.

    Parameters:
        maze (list of lists of int): The 3D maze to convert.
        paths list of (list of (int, int, int)): The paths to highlight in the maze.
        wall_block_id (str): The block ID to use for walls.
        floor_block_id (str): The block ID to use for floors.

    Returns:
        schematic (mcschematic.MCSchematic): The resulting schematic.
    """
    dim_x = len(maze)
    dim_y = len(maze[0])
    dim_z = len(maze[0][0])

    # Create a blank schematic
    schematic = mcschematic.MCSchematic()

    for x in range(dim_x):
        for y in range(dim_y):
            for z in range(dim_z):
                if maze[x][y][z] == 1:  # Wall
                    schematic.setBlock((x, y, z), wall_block_id)
                elif maze[x][y][z] == 0:  # Floor
                    schematic.setBlock((x, y, z), floor_block_id)

    for path in paths:
        if path:
            # Ensure that path coordinates are tuples, not lists
            path = [tuple(coord) for coord in path]

            for (x, y, z) in path:
                schematic.setBlock((x, y, z), "minecraft:redstone_block")

            schematic.setBlock(path[0], "minecraft:redstone_block")
            schematic.setBlock(path[-1], "minecraft:gold_block")

    return schematic


def save_schematic(schematic, folder, filename):
    """Save the schematic to a file."""
    schematic.save(folder, filename, mcschematic.Version.JE_1_18_2)
