from peewee import SqliteDatabase

from database.level_dto import LevelDto
from database.background_info import BackgroundInfo
from database.monster_info import MonsterInfo
from database.leaderboard_record import LeaderboardRecord
from database.player import Player
from database.level import Level
from database.background import Background
from database.monster import Monster
from database.terrain_info import TerrainInfo
from database.terrain import Terrain


# здесь будут методы для работы с базой данных
# todo КЛАСС DATABASE НУЖНО ПЕРЕДАВАТЬ ЧЕРЕЗ КОНСТРУКТОР И ПОТОМ ПЕРЕДАВАТЬ ВО ВСЕ КЛАССЫ
class DbHelper:

    def CreateAllTables(self):
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
        database.connect()
        database.create_tables(
            [Player,
             LeaderboardRecord,
             Level,
             Terrain,
             Background,
             Monster,
             TerrainInfo,
             BackgroundInfo,
             MonsterInfo])

    def GetLeaderboards(self, leveId):
        leaderboards = LeaderboardRecord \
            .select() \
            .where(LeaderboardRecord.levelId == leveId) \
            .order_by(LeaderboardRecord.score.desc())
        return leaderboards

    def UpdateLeaderboardRecord(self, id, levelId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(id=id, levelId=levelId, playerId=playerId, score=newScore)
        return leaderboardRecord.save()  # мы передаем id, поэтому save делает UPDATE вместо CREATE

    def CreateLeaderboardRecord(self, levelId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(levelId=levelId, playerId=playerId, score=newScore)
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

    # TODO НАМ ЕЩЕ НАДО МЕТОД UPDATE USER
    def RegisterUser(self, nickname, password):
        player = Player(nickname=nickname, password=password,
                        unlockedLevel=1, hp=10, attack=10, defence=10, playerLevel=1, xp=0)
        player.save()

    def UpdateUser(self, nickname, hp, xp, defence, attack, level):
        player = Player.select().where(Player.nickname == nickname)[0]
        player.xp = xp
        player.hp = hp
        player.defence = defence
        player.attack = attack
        player.playerLevel = level
        player.save()

    def GetUser(self, nickname, password):
        players = Player.select().where(Player.nickname == nickname)
        player = players[0]
        if player.password == password:
            return player
        return None

    def GetLevel(self, level_id):
        level = Level.select().where(Level.id == level_id)
        backgroundsInfo = self.GetBackgroundsInfo()
        monstersInfo = self.GetMonstersInfo()
        terrainsInfo = self.GetTerrainsInfo()
        return LevelDto(level, backgroundsInfo, monstersInfo, terrainsInfo)

    # нужно запускать только 1 раз при инициализации сервера
    # note: levelId у элементов списка не нужно задавать
    # todo - сделать сохранение список за 1 один запрос к базе данных
    def CreateLevel(self, size_x, size_y, backgrounds, monsters, terrains):
        level = Level(sizeX=size_x, sizeY=size_y)
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
        # порядок важен
        print("delete leaderboards " + str(LeaderboardRecord.delete().execute()))
        print("delete player " + str(Player.delete().execute()))
        print("delete bg " + str(Background.delete().execute()))
        print("delete monsters " + str(Monster.delete().execute()))
        print("delete terrain " + str(Terrain.delete().execute()))
        print("delete lvl " + str(Level.delete().execute()))
        print("delete terrain info " + str(TerrainInfo.delete().execute()))
        print("delete monster info " + str(MonsterInfo.delete().execute()))
        print("delete bg info " + str(BackgroundInfo.delete().execute()))
