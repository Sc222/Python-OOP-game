from main.gui.constants import TILE_SIZE_HALF, TILE_SIZE
from main.gui.game.static_entity import StaticEntity
from main.resources.tiles_constants import TERRAIN_CAN_WALK_ON, TILE_EMPTY


class MapParser:
    @staticmethod
    def can_walk_on(tile, is_terrain):
        if is_terrain:
            return tile in TERRAIN_CAN_WALK_ON
        return True

    @staticmethod
    def map_to_draw_objects(images, game_map, width, height, shift_y=0, is_terrain=False):
        res = {}
        print(game_map)
        for map_x in range(width):
            for map_y in range(height):
                tile = game_map[map_x, map_y]
                if tile != TILE_EMPTY:
                    tile_image = images[tile]
                    x = (map_x - map_y) * TILE_SIZE_HALF
                    y = (map_x + map_y) * 0.5 * TILE_SIZE_HALF + shift_y
                    res[(map_x, map_y)] = StaticEntity(tile_image, x, y, MapParser.can_walk_on(tile, is_terrain))
        return res
