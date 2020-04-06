from main.background import Background
from main.terrain import Terrain
from main.monster import Monster
from main.background_info import BackgroundInfo
from main.terrain_info import TerrainInfo
from main.monster_info import MonsterInfo
from main.leaderboard_record import LeaderboardRecord
from main.player import Player
from main.level import Level


# здесь будут методы для работы с базой данных
class DbHelper:

    def GetLeaderboards(self, leveId):
        leaderboards = LeaderboardRecord\
            .select()\
            .where(LeaderboardRecord.levelId == leveId)\
            .order_by(LeaderboardRecord.score.desc())
        return leaderboards

    def UpdateLeaderboardRecord(self, id, leveId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(id=id, leveId=leveId, playerId=playerId, score=newScore)
        return leaderboardRecord.save()  # мы передаем id, поэтому save делает UPDATE вместо CREATE

    def CreateLeaderboardRecord(self, leveId, playerId, newScore):
        leaderboardRecord = LeaderboardRecord(leveId=leveId, playerId=playerId, score=newScore)
        return leaderboardRecord.save()

    def GetMonstersInfo(self):
        return MonsterInfo.select()

    def GetTerrainsInfo(self):
        return TerrainInfo.select()

    def GetBackgroundsInfo(self):
        return BackgroundInfo.select()

