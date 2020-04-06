from main.db_helper import DbHelper
import unittest


class DbHelperTest(unittest.TestCase):
    def setUp(self):
        self.dbHelper = DbHelper()

