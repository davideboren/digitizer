#Class for Monster instances

import pygame as pg
from random import randint

class Monster(pg.sprite.Sprite):
    def __init__(self, data):
    
        super(Monster,self).__init__()

        self.data = data

        self.evos = []
        
        self.border_color = (200,200,200)
        self.bg_color = (45,45,45)
        self.spritesheet_coords = (0,0)
        self.ticks = randint(0,29)
        
        self.img = pg.image.load(self.data.filepath)
        self.rect = pg.Rect(0,0,34,34)
        self.surf = pg.Surface((34,34), pg.SRCALPHA)
        self.surf.fill(self.border_color)
        self.sprite = pg.Surface((16,16), pg.SRCALPHA)
        self.sprite.fill(self.bg_color)
        self.sprite.blit(self.img, (0,0), (self.spritesheet_coords, (16,16)))
        self.surf.blit(pg.transform.scale(self.sprite, (32,32)), (1,1))
        
        self.rect.move_ip(self.data.coords)
        self.dragging = False

    def add_evo(self, mon):
        self.data.evos.append(mon.data.name)
        self.evos.append(mon)
    
    def remove_evo(self,mon):
        self.data.evos.remove(mon.data.name)
        self.evos.remove(mon)

    def set_border(self,color):
        self.border_color = color
        self.surf.fill(self.border_color)
        self.surf.blit(pg.transform.scale(self.sprite,(32,32)),(1,1))

    def update(self):
        self.ticks += 1
        if(self.ticks == 30):
            if self.bg_color == (0,0,0,0):
                self.surf = pg.Surface((34,34), pg.SRCALPHA)
                self.sprite = pg.Surface((16,16), pg.SRCALPHA)
            self.spritesheet_coords = (((self.spritesheet_coords[0] + 16) % (32 + randint(0,1)*16),0))
            self.sprite.fill(self.bg_color)
            self.sprite.blit(self.img, (0,0), (self.spritesheet_coords,(16,16)))
            self.surf.blit(pg.transform.scale(self.sprite,(32,32)),(1,1))
            self.ticks = 0