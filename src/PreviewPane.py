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

        self.set_bg("bg/bg_0.bmp")

    def set_bg(self,bg_filepath):
        self.bg = pg.sprite.Sprite()
        self.bg.img = pg.image.load(bg_filepath)
        self.bg.surf = pg.Surface((128+2,128+2))
        self.bg.surf.fill(FG_WHITE)
        self.bg.rect = pg.Rect(1,1,128+2,128+2)
        self.bg.surf.blit(pg.transform.scale(self.bg.img,(128,128)),
                          self.bg.rect)

    def set_mon(self,filename):
        data2 = MonsterData(
            filepath = filename,
            coords = (self.rect.centerx - 16, self.rect.bottom - 76)
        )
        self.mon = Monster(data2)
        self.mon.make_transparent()
        
    def update(self, event_list):
        for event in event_list:
            if event.type == BG_SELECT:
                self.set_bg(event.filepath)
            elif event.type == MON_SELECT:
                self.set_mon(event.filepath)
                self.set_bg(event.bg.strip('"'))
        if self.mon != None:
            self.mon.update()

    def draw(self, surf):
        surf.blit(self.surf, self.rect)
        surf.blit(self.bg.surf, (self.rect.left + 36, self.rect.top + 36))
        if self.mon != None:
            surf.blit(self.mon.surf, self.mon.rect)
