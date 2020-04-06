from main.background_info import BackgroundInfo
from main.db_helper import DbHelper
from main.monster_info import MonsterInfo
from main.player import Player
from testfixtures import compare
import unittest

from main.terrain_info import TerrainInfo


class DbHelperTest(unittest.TestCase):
    def setUp(self):
        self.dbHelper = DbHelper()
        self.dbHelper.CreateAllTables()

    def tearDown(self):
        self.dbHelper.ClearAllBase()

    def test_AddUser(self):
        self.dbHelper.RegisterUser("user", "qwerty")
        user: Player = self.dbHelper.GetUser("user", "qwerty")
        self.assertEqual(user.nickname, "user")
        self.assertEqual(user.password, "qwerty")

    def test_CreateMonsterInfo(self):
        self.dbHelper.CreateMonsterInfo("img.png", 100, 15, 10)
        monstersInfo = self.dbHelper.GetMonstersInfo()
        self.assertEqual(len(monstersInfo), 1, "monsterInfo wasn't created")

    def test_CreateMultipleMonsterInfo(self):
        self.dbHelper.CreateMonsterInfo("img1.png", 100, 15, 10)
        self.dbHelper.CreateMonsterInfo("img2.png", 200, 18, 30)
        self.dbHelper.CreateMonsterInfo("img3.png", 300, 29, 50)
        result = self.dbHelper.GetMonstersInfo()
        expected = [MonsterInfo(id=1, image="img1.png", hp=100, attack=15, defence=10),
                    MonsterInfo(id=2, image="img2.png", hp=200, attack=18, defence=30),
                    MonsterInfo(id=3, image="img3.png", hp=300, attack=29, defence=50)]
        compare(result, expected)

    def test_CreateBackgroundInfo(self):
        self.dbHelper.CreateBackgroundInfo("grass.png")
        backgroundInfo = self.dbHelper.GetBackgroundsInfo()
        self.assertEqual(len(backgroundInfo), 1, "backgroundInfo wasn't created")

    def test_CreateMultipleBackgroundInfo(self):
        self.dbHelper.CreateBackgroundInfo("grass.png")
        self.dbHelper.CreateBackgroundInfo("water.png")
        self.dbHelper.CreateBackgroundInfo("floor.png")
        result = self.dbHelper.GetBackgroundsInfo()
        expected = [BackgroundInfo(id=1, image="grass.png"),
                    BackgroundInfo(id=2, image="water.png"),
                    BackgroundInfo(id=3, image="floor.png")]
        compare(result, expected)

    def test_CreateTerrainInfo(self):
        self.dbHelper.CreateTerrainInfo("grass.png")
        terrainInfo = self.dbHelper.GetTerrainsInfo()
        self.assertEqual(len(terrainInfo), 1, "terrainInfo wasn't created")

    def test_CreateMultipleTerrainInfo(self):
        self.dbHelper.CreateTerrainInfo("stone.png")
        self.dbHelper.CreateTerrainInfo("tree.png")
        self.dbHelper.CreateTerrainInfo("wall.png")
        result = self.dbHelper.GetTerrainsInfo()
        expected = [TerrainInfo(id=1, image="stone.png"),
                    TerrainInfo(id=2, image="tree.png"),
                    TerrainInfo(id=3, image="wall.png")]
        compare(result, expected)

# def test_create(self):
#    self.dbHelper.CreateLeaderboardRecord(0, 1, 100)
#    records = list(self.dbHelper.GetLeaderboards(0))
#    self.assertEqual(len(records), 1, "leaderboard wasn't created")
