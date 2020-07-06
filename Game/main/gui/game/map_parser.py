from main.gui.constants import TILE_SIZE_HALF, TILE_SIZE
from main.gui.game.static_entity import StaticEntity


class MapParser:
    @staticmethod
    def can_walk_on(tile, is_terrain):
        if is_terrain:
            return not tile == 1
        return True

    @staticmethod
    def map_to_draw_objects(images, game_map,width,height,SHIFT_Y=0,is_terrain=False):
        #print(len(game_map))
        #print(len(game_map[0]))
        res = {}
        print(game_map)
        for map_x in range(width):
            for map_y in range(height):
                tile = int(game_map[map_x,map_y])
                if tile != 0:
                    tile_image = images[tile - 1]
                    x = (map_x - map_y) * TILE_SIZE_HALF
                    y = (map_x + map_y) * 0.5 * TILE_SIZE_HALF+SHIFT_Y
                    res[(map_x,map_y)]=StaticEntity(tile_image, x, y, MapParser.can_walk_on(tile,is_terrain))
        return res

    @staticmethod
    def map_to_draw_objects_from_server(images, game_map, center_x, center_y):
        result_ls = list()
        for map_obj in game_map:
            tile_image = images[map_obj.name]
            x_shift = center_x - TILE_SIZE_HALF
            y_shift = center_y * 0.5 - TILE_SIZE
            x = x_shift + (map_obj.x - map_obj.y) * TILE_SIZE_HALF
            y = y_shift + (map_obj.x + map_obj.y) * 0.5 * TILE_SIZE_HALF
            result_ls.append(StaticEntity(tile_image, x, y))
        return result_ls

    @staticmethod
    def monsters_to_draw_objects(images, monsters, center_x, center_y):
        result_ls = list()
        for monster in monsters:
            monster_images = images[monster.name]
            x_shift = center_x - TILE_SIZE_HALF
            y_shift = center_y * 0.5 - TILE_SIZE
            centered_x = x_shift + (monster.x - monster.y) * TILE_SIZE_HALF
            centered_y = y_shift + (monster.x + monster.y) * 0.5 * TILE_SIZE_HALF
            result_ls.append(StaticEntity(monster_images, centered_x, centered_y))
        return result_ls