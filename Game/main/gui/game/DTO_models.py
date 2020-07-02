class map_obj_from_json():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class monster_obj_from_json():
    def __init__(self, x, y, name, hp, attack, defence):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defence = defence


class level_from_json():
    def __init__(self, backgrounds, monsters, terrains):
        self.backgrounds = backgrounds
        self.monsters = monsters
        self.terrains = terrains
