import pygame as pg
import os
from MonsterImg import MonsterImg
from config import *

class AvailMonsPane(pg.sprite.Sprite):
    def __init__(self, coords):
        super(AvailMonsPane,self).__init__()

        #PANE_WIDTH = round(SCREEN_WIDTH/3) - 32
        PANE_WIDTH = 275
        PANE_HEIGHT = SCREEN_HEIGHT - 32

        self.surf = pg.Surface((PANE_WIDTH,PANE_HEIGHT))
        pg.draw.rect(self.surf,(25,0,25),(0,0,PANE_WIDTH,PANE_HEIGHT), border_radius=4)
        pg.draw.rect(self.surf,(170,170,170),(0,0,PANE_WIDTH,PANE_HEIGHT), width=2, border_radius=4)
        self.rect = self.surf.get_rect()

        self.mons = []
        x = y = 0
        cols = 6
        for r,d,f in os.walk("sprites/baby"):
            for file in f:
                if 'png' in file:
                    self.mons.append(MonsterImg(os.path.join(r,file),(20 + x, 20 + y)))
                    
                    x = (x + 40) % (cols * 40)
                    if x == 0:
                        y += 40

        #self.mons.append(MonsterImg("sprites/baby/Yukimibotamon.png",(32,32)))

    def handleEvents(self, event):
        return
    def update(self):
        for mon in self.mons:
            mon.update()
            self.surf.blit(mon.surf,mon.rect)
