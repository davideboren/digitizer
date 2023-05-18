import pygame as pg

from config import *

class BackgroundPane(pg.sprite.Sprite):

    def __init__(self):
        super(BackgroundPane, self).__init__()

        self.surf = pg.Surface((BG_PANE_W, BG_PANE_H))
        self.rect = self.surf.get_rect().move(1036 + PAD, 24 + PAD)

        pg.draw.rect(self.surf, PANE_BG_DARK,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4)
        pg.draw.rect(self.surf, FG_WHITE,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4, width = 2)

    def update(self):
        return

    def draw(self, surf):
        surf.blit(self.surf, self.rect)
