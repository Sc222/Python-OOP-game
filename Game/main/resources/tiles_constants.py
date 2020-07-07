# todo add warning in readme
# WARNING: EMPTY IS ALWAYS SKIPPED
# WARNING: ALL TILES NAME MUST BE 1 CHAR LENGTH STRING (because random.choice from string is used)

TILE_EMPTY = "e"

# background tiles
BG_WATER = "1"
BG_SAND = "2"
BG_GRASS = "3"
BG_DK_GRASS = "4"

# terrain tiles
TR_EMPTY = TILE_EMPTY
TR_INVISIBLE = " "

# sand location
TR_CACTUS = "0"
TR_CACTUS_FL = "1"

# grass location
TR_OAK = "2"
TR_BIRCH = "3"
TR_HOUSE = "4"

# dark grass location
TR_PINE = "5"
TR_BUSH = "6"
TR_FERN = "7"

# set of tiles that player can walk on
TERRAIN_CAN_WALK_ON = {
    TR_EMPTY
}

# dictionary of trees radius spawn rate by locations
TREE_RADIUS_BY_BG = {
    BG_WATER: None,
    BG_SAND: 2,
    BG_GRASS: 1,
    BG_DK_GRASS: 1
}

# dictionary of locations where items can be spawned
SPAWN_LOCATIONS = [BG_SAND, BG_GRASS, BG_DK_GRASS]

# string for declaring possibilities of different trees spawn
TREES_POSSIBILITY_SAND = TR_CACTUS + TR_CACTUS_FL
TREES_POSSIBILITY_GRASS = TR_OAK * 3 + TR_BIRCH * 3 + TR_HOUSE
TREES_POSSIBILITY_DK_GRASS = TR_PINE * 5 + TR_FERN + TR_BUSH

# dictionary of trees that can be spawned in different locations
TREES_BY_BG = {
    BG_WATER: None,
    BG_SAND: TREES_POSSIBILITY_SAND,
    BG_GRASS: TREES_POSSIBILITY_GRASS,
    BG_DK_GRASS: TREES_POSSIBILITY_DK_GRASS
}
