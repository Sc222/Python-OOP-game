from peewee import *


class MonsterInfo(Model):
    image = TextField()  # путь до  папки со спрайтами (картинки будут храниться локально)
    # todo важно!!!(image будет отвечать за ПАПКУ, а в папке будут папки с анимациями attack, die, move и так далее)
    hp = IntegerField()
    attack = IntegerField()
    defence = IntegerField()

    class Meta:
        table_name = 'monstersInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
