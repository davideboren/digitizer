import pygame as pg

from config import *
from Monster import Monster
from MonsterData import MonsterData

class PreviewPane(pg.sprite.Sprite):

    def __init__(self):
        super(PreviewPane, self).__init__()

        self.surf = pg.Surface((PREVIEW_PANE_W, PREVIEW_PANE_H))
        self.rect = self.surf.get_rect().move(
            1052, SCREEN_H - PAD - 200)

        pg.draw.rect(self.surf, PANE_BG_DARK,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4)
        pg.draw.rect(self.surf, FG_WHITE,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4, width = 2)
        
        self.bg = None
        self.mon = None

    def set_bg(self,bg_sprite):
        self.bg = bg_sprite

    def set_mon(self,filename):
        data2 = MonsterData(
            filepath = filename,
            coords = (self.rect.centerx - 16, self.rect.bottom - 76)
        )
        self.mon = Monster(data2)
        self.mon.set_border((0,0,0,0))
        self.mon.bg_color = (0,0,0,0)
        
    def update(self):
        if self.mon != None:
            self.mon.update()

    def draw(self, surf):
        surf.blit(self.surf, self.rect)
        surf.blit(self.bg.surf, (self.rect.left + 36, self.rect.top + 36))
        if self.mon != None:
            surf.blit(self.mon.surf, self.mon.rect)
