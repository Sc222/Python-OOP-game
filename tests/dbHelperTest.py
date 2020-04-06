from main.db_helper import DbHelper
import unittest


class DbHelperTest(unittest.TestCase):
    def setUp(self):
        self.dbHelper = DbHelper()
        self.dbHelper.ClearAllBase()

    def createLeaderboard(self):
        self.dbHelper.CreateLeaderboardRecord(0, 1, 100)
        records = list(self.dbHelper.GetLeaderboards(0))
        self.assertEqual(len(records), 1, "leaderboard wasn't created")
