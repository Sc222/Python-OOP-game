from main.db_helper import DbHelper
from main.player import Player
import unittest


class DbHelperTest(unittest.TestCase):
    def setUp(self):
        self.dbHelper = DbHelper()
        self.dbHelper.ClearAllBase()

    def test_AddUser(self):
        self.dbHelper.RegisterUser("govno","GOVNO")
        user: Player = self.dbHelper.GetUser("govno","GOVNO")
        self.assertEqual(user.nickname == "govno")
        self.assertEqual(user.password == "GOVNO")

    def createLeaderboard(self):
        self.dbHelper.CreateLeaderboardRecord(0, 1, 100)
        records = list(self.dbHelper.GetLeaderboards(0))
        self.assertEqual(len(records), 1, "leaderboard wasn't created")
