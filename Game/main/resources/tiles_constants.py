# todo add warning in readme
# WARNING: EMPTY IS ALWAYS SKIPPED
# WARNING: ALL TILES NAME MUST BE UNIQUE 1 CHAR LENGTH STRING (because random.choice from string is used)
# used chars: e, c, f, o, b, h, 0, 2, p, 4, l, 3

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
TR_CACTUS = "c"
TR_CACTUS_FL = "f"

# grass location
TR_OAK = "o"
TR_BIRCH = "b"
TR_HOUSE = "h"
TR_BUSH = "0"
TR_BERRY_BUSH = "1"
TR_FERN = "2"

# dark grass location
TR_PINE = "p"
TR_STONE = "4"
TR_LOG = "l"
TR_STUMP = "3"

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
TREES_POSSIBILITY_GRASS = TR_OAK * 3 + TR_BIRCH * 3 + TR_HOUSE + TR_BUSH*2 + TR_FERN*2 + TR_BERRY_BUSH*2
TREES_POSSIBILITY_DK_GRASS = TR_PINE * 5 + TR_STONE + TR_LOG + TR_STUMP

# dictionary of trees that can be spawned in different locations
TREES_BY_BG = {
    BG_WATER: None,
    BG_SAND: TREES_POSSIBILITY_SAND,
    BG_GRASS: TREES_POSSIBILITY_GRASS,
    BG_DK_GRASS: TREES_POSSIBILITY_DK_GRASS
}
