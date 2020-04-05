from peewee import *

db = SqliteDatabase('database.db') #везде должна быть бдшка одного имени

# пример создания объекта person из которого потом создастся таблица persons
class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.