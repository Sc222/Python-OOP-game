GAME_NAME = "Mega Nerd"
LEADERBOARDS = "Leaderboards"
RESOURCES_FOLDER = "../../resources"
MONOSPACE_FONT = "Determination Mono(RUS BY LYAJK"
FPS = 60
TERRAIN_SHIFT = -6
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
SCALE = 5
GUI_SCALE = 3
PLAYER_MENU_SCALE = 14
TILE_COLLIDE_W = 21 * SCALE
TILE_SIZE = 32 * SCALE
TILE_SIZE_HALF = TILE_SIZE / 2
MOUSE_IDLE_DELTA = 40  # когда разница в координатах меньше этого числа игрок стоит на месте
MONSTER_ATTACK_DELTA_X = 20  # когда разница в координатах меньше этого числа монстр начинает атаку
MONSTER_ATTACK_DELTA_Y = 30  # когда разница в координатах меньше этого числа монстр начинает атаку
CREATURE_SHIFT = -5*SCALE                # SHIFT CREATURE Y WHEN SPAWN
M_HEIGHT = 45 * SCALE  # m - monster
M_WIDTH = 76 * SCALE
PL_SIZE = 24 * SCALE  # pl - player
PL_COLLIDE_W = 6 * SCALE
PL_COLLIDE_H = 5 * SCALE
MOVE_COLLIDE_RECT_OFFSET = 2  # cкорость движения по осям умножается на это число и хитбокс сдвигается
LEADERBOARD_INTIAL_FONT_SIZE = 26  # первоначальный размер шрифта, далее он масштабируется

# colors
MAIN_MENU_HEADER = (0, 105, 170)
YELLOW_LIGHT = (246, 202, 159)
WHITE = (255, 255, 255)
RED = (234, 0, 60)
RED_DARK = (196, 36, 48)
RED_CONTRAST = (244, 0, 12)
GREEN = (30, 111, 80)
TRANSPARENT = (0, 0, 0, 0)
SKY = (0, 205, 249)
DEBUG = (255, 0, 64)
PL = (0, 255, 0)
TR = (0, 0, 255)

# no internet actions
ACTION_ENTRY = "Can't login"
ACTION_GET_LEADERBOARDS = "Can't get leaderboards"
ACTION_GET_USER = "Can't get user information"
