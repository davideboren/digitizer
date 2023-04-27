#Class for Monster instances

import pygame as pg
from random import randint
from dataclasses import dataclass

@dataclass 
class MonsterData:
    filepath: str
    name: str
    stage: str
    move_style: str
    bg: str
    evos: list[str]

    tab: int
    coords: int

class Monster(pg.sprite.Sprite):
    def __init__(self, filepath, coords):
    
        super(Monster,self).__init__()

        # Saveable data
        self.data = MonsterData(
            filepath,
            filepath.split('/')[-1].split('.')[0],
            filepath.split('/')[-2],
            "walk",
            "",
            [],
            0,
            coords
        )
        
        self.border_color = (200,200,200)
        self.spritesheet_coords = (0,0)
        self.ticks = randint(0,29)
        
        self.img = pg.image.load(self.data.filepath)
        self.rect = pg.Rect(0,0,34,34)
        self.surf = pg.Surface((34,34))
        self.surf.fill(self.border_color)
        self.sprite = pg.Surface((16,16))
        self.sprite.fill((45,45,45))
        self.sprite.blit(self.img, (0,0), (self.spritesheet_coords, (16,16)))
        self.surf.blit(pg.transform.scale(self.sprite, (32,32)), (1,1))
        
        self.rect.move_ip(self.data.coords)
        self.dragging = False

    def set_border(self,color):
        self.border_color = color
        self.surf.fill(self.border_color)
        self.surf.blit(pg.transform.scale(self.sprite,(32,32)),(1,1))

    def update(self):
        self.ticks += 1
        if(self.ticks == 30):
            self.spritesheet_coords = (((self.spritesheet_coords[0] + 16) % (32 + randint(0,1)*16),0))
            self.sprite.fill((45,45,45))
            self.sprite.blit(self.img, (0,0), (self.spritesheet_coords,(16,16)))
            self.surf.blit(pg.transform.scale(self.sprite,(32,32)),(1,1))
            self.ticks = 0