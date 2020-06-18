class LevelDto:

    def __init__(self, dbLevel, backgroundsInfo, monstersInfo, terrainsInfo):
        self.dbLevel = dbLevel
        self.backgroundsInfo = backgroundsInfo
        self.monstersInfo = monstersInfo
        self.terrainsInfo = terrainsInfo
        # чтобы получить monsters, terrains, backgrounds использовать list(dbLevel.monsters)
