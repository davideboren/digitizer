import pygame as pg
from config import *


class Sandbox(pg.sprite.Sprite):

    def __init__(self):
        super(Sandbox, self).__init__()

        self.surf = pg.Surface((736, SCREEN_H - PAD*2 - 24))
        self.rect = self.surf.get_rect().move(284 + PAD, 24 + PAD)

        self.tab = 0
        self.mons = []
        self.mons.append(pg.sprite.LayeredUpdates())

        pg.draw.rect(self.surf, (20,20,30), 
                    (0,0,self.rect.w, self.rect.h), border_radius = 4)
        for l in range(0, self.rect.w, 50): #Gridlines
            pg.draw.line(self.surf, (30,30,40), (l,0),
                        (l, self.rect.h), width = 2)
        for l in range(0, self.rect.h, 50):
            pg.draw.line(self.surf, (30,30,40), (0,l),
                        (self.rect.right, l), width = 2)
        pg.draw.rect(self.surf, FG_WHITE, 
                    (0, 0, self.rect.w, self.rect.h), 
                    border_radius=4, width = 2)
        
    def add_mon(self, mon):
        self.mons[self.tab].add(mon)

    def get_mons(self, tab = -1):
        if tab == -1:
            tab = self.tab
        return self.mons[tab]

    def get_all_mon_names(self):
        names = []
        for tab in self.mons:
            for mon in tab:
                names.append(mon.name)
        return names

    def draw(self, surf):
        surf.blit(self.surf, self.rect)