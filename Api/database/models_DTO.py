class Leaderboard_Dto():
    def __init__(self, id, playerId, levelId, score):
        self.id = id
        self.playerId = playerId
        self.levelId = levelId
        self.score = score


class Background_Dto():
    x = 0
    y = 0
    imageSource = ''

    def __init__(self, x, y, imageSource):
        self.x = x
        self.y = y
        self.imageSource = imageSource


class LevelDto:

    def __init__(self, backgrounds, monsters, terrains):
        self.backgrounds = backgrounds
        self.monsters = monsters
        self.terrains = terrains
