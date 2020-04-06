from main.db_helper import DbHelper
from main.player import Player
import unittest


class DbHelperTest(unittest.TestCase):
    def setUp(self):
        self.dbHelper = DbHelper()

    def test_AddUser(self):
        self.dbHelper.RegisterUser("govno","GOVNO")
        user: Player = self.dbHelper.GetUser("govno","GOVNO")
        self.assertEqual(user.nickname == "govno")
        self.assertEqual(user.password == "GOVNO")
if __name__ == "__main__":
  unittest.main()