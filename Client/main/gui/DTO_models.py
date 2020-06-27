

class map_obj_from_json():
    def __init__(self,x,y,name):
        self.x=x
        self.y=y
        self.name=name


class level_from_json():
    def __init__(self,backgrounds,monsters,terrains):
        self.backgrounds = backgrounds
        self.monsters = monsters
        self.terrains = terrains