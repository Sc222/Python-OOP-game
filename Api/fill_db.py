from app import db
from database import models

def create_backgroundInfo():
    background_names = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    background_info = [models.BackgroundInfo(name=name) for name in background_names]
    db.session.add_all(background_info)
    db.session.commit()

def create_terrainInfo():
    terrain_names = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush", "invisible"]
    terrain_info = [models.TerrainInfo(name=name) for name in terrain_names]
    db.session.add_all(terrain_info)
    db.session.commit()

def create_monsterInfo():
    monster_info = [models.MonsterInfo(name="skeleton",hp=50,attack=35,defence=10),
                    models.MonsterInfo(name="goblin",hp=100,attack=50,defence=25)]
    db.session.add_all(monster_info)
    db.session.commit()

def create_level1():
    l1 = models.Level(sizeX=9,sizeY=9)
    db.session.add(l1)
    db.session.commit()

def create_backgrounds1():
    background_types = [[0,0,0,0,0,0,0,0,0],
                        [0,1,1,2,3,1,1,1,0],
                        [0,1,1,4,5,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,0,0,0,0,0,0,0,0]]

    backgrounds=[models.Background(level_id=1,x=x,y=y,infoId=background_types[x][y])
                 for x in range(9) for y in range(9)
                 if background_types[x][y]!=0 ]
    db.session.add_all(backgrounds)
    db.session.commit()

def create_terrain1():
    terrain_types =    [[8,8,8,8,8,8,8,8,8],
                        [8,2,5,8,8,4,0,1,8],
                        [8,0,0,8,8,0,6,0,8],
                        [8,3,0,0,0,7,0,0,8],
                        [8,0,0,6,0,0,0,0,8],
                        [8,4,0,0,0,0,0,5,8],
                        [8,0,0,0,0,0,0,0,8],
                        [8,2,7,4,0,0,0,0,8],
                        [8,8,8,8,8,8,8,8,8]]
    terrains = [models.Terrain(levelId=1, x=x, y=y, infoId=terrain_types[x][y])
                   for x in range(9) for y in range(9)
                   if terrain_types[x][y] != 0]
    db.session.add_all(terrains)
    db.session.commit()

create_level1()
