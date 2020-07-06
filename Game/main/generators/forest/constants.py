BG_WATER = "1"
BG_SAND = "2"
BG_GRASS = "3"
BG_DARK_GRASS = "4"
TERRAIN_EMPTY = "0"
TERRAIN_INVISIBLE_WALL = "1"

# TODO STRING CAN BE USED
# TODO MAKE TERRAIN CONSTANTS
TREES_BY_BG = {
    BG_WATER: None,
    BG_SAND: ["2"],
    BG_GRASS: ["3", "3", "3", "3", "4", "4", "4", "4", "5", "5", "5", "6", "6", "6", "2"],
    BG_DARK_GRASS: ["7", "7", "7", "7", "8"]
}
TREE_RADIUS_BY_BG = {
    BG_WATER: None,
    BG_SAND: 3,
    BG_GRASS: 2,
    BG_DARK_GRASS: 1
}
