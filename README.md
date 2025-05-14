# 3D Maze Schematic Generator
A simple CLI tool to generate a 3D maze, solve it, and export it as a Minecraft .schematic file. Optionally shows a 3D visualization of the maze using matplotlib.

## Usage
```bash
python maze_cli.py --folder <output_folder> [options]
```

## Required

* `--folder <path>`
Path to the folder where the schematic will be saved.

## Optional
* `--dim_x <int>` (default: 21)
Maze width (must be odd)

* `--dim_y <int>` (default: 21)
Maze height (must be odd)

* `--dim_z <int>` (default: 21)
Maze depth (must be odd)

* `--filename <str>` (default: 3dmaze)
Output schematic filename (without extension)

* `--wall_block <str>` (default: minecraft:glass)
Minecraft block ID for walls

* `--floor_block <str>` (default: minecraft:air)
Minecraft block ID for empty space

* `--visualize`
Show a 3D matplotlib preview of the maze after generation

## Example
```bash
python maze_cli.py --folder "./schematics" --dim_x 25 --dim_y 25 --dim_z 25 --filename my_maze --visualize
```