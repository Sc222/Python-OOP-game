from main.level_dto import LevelDto
from main.background_info import BackgroundInfo
from main.terrain_info import TerrainInfo
from main.monster_info import MonsterInfo
from main.leaderboard_record import LeaderboardRecord
from main.player import Player
from main.level import Level
from main.background import Background
from main.monster import Monster
from main.terrain_info import TerrainInfo
from main.terrain import Terrain


# здесь будут методы для работы с базой данных
class DbHelper:

    def GetLeaderboards(self, leveId):
        leaderboards = LeaderboardRecord \
            .select() \
            .where(LeaderboardRecord.levelId == leveId) \
            .order_by(LeaderboardRecord.score.desc())
        return leaderboards

    def UpdateLeaderboardRecord(self, id, leveId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(id=id, leveId=leveId, playerId=playerId, score=newScore)
        return leaderboardRecord.save()  # мы передаем id, поэтому save делает UPDATE вместо CREATE

    def CreateLeaderboardRecord(self, leveId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(leveId=leveId, playerId=playerId, score=newScore)
        return leaderboardRecord.save()

    def GetMonstersInfo(self):
        return list(MonsterInfo.select())

    # нужно запускать только 1 раз при инициализации сервера
    def CreateMonsterInfo(self, image, hp, attack, defence):
        monsterInfo = MonsterInfo(image=image, hp=hp, attack=attack, defence=defence)
        return monsterInfo.save()

    def GetTerrainsInfo(self):
        return list(TerrainInfo.select())

    # нужно запускать только 1 раз при инициализации сервера
    def CreateTerrainInfo(self, image):
        terrainInfo = TerrainInfo(image=image)
        return terrainInfo.save()

    def GetBackgroundsInfo(self):
        return list(BackgroundInfo.select())

    # нужно запускать только 1 раз при инициализации сервера
    def CreateBackgroundInfo(self, image):
        backgroundInfo = BackgroundInfo(image=image)
        return backgroundInfo.save()

    def RegisterUser(self, nickname, password):
        player = Player(nickname, password)
        player.save()

    def GetUser(self, nickname, password):
        players = Player.select().where(Player.nickname == nickname)
        player = players[0]
        if player.password == password:
            return player
        return None

    def GetLevel(self, levelId):
        level = Level.select().where(Level.id == levelId)
        backgroundsInfo = self.GetBackgroundsInfo()
        monstersInfo = self.GetMonstersInfo()
        terrainsInfo = self.GetTerrainsInfo()
        return LevelDto(level, backgroundsInfo, monstersInfo, terrainsInfo)

    # нужно запускать только 1 раз при инициализации сервера
    # note: levelId у элементов списка не нужно задавать
    # todo - сделать сохранение список за 1 один запрос к базе данных
    def CreateLevel(self, sizeX, sizeY, backgrounds, monsters, terrains):
        level = Level(sizeX=sizeX, sizeY=sizeY)
        level.save()
        levelId = level.id
        for background in backgrounds:
            background.levelId = levelId
            background.save()
        for monster in monsters:
            monster.levelId = levelId
            monster.save()
        for terrain in terrains:
            terrain.levelId = levelId
            terrain.save()

    def ClearAllBase(self):
        Level.delete().execute()
        Background.delete().execute()
        LeaderboardRecord.delete().execute()
        MonsterInfo.delete().execute()
        BackgroundInfo.delete().execute()
        Monster.delete().execute()
        TerrainInfo.delete().execute()
        Terrain.delete().execute()

