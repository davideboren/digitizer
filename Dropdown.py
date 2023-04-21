import pygame as pg
from config import *

class Dropdown(pg.sprite.Sprite):
    def __init__(self,title):

        super(Dropdown,self).__init__()

        self.title = title
        self.font = pg.font.Font("grand9k.ttf",14)
        self.fg = FG_WHITE
        self.bg = PANE_BG_DARK
        self.surf = self.font.render(title,False,self.fg,self.bg)
        self.rect = self.surf.get_rect()
        self.pressed = False
    
    def handleEvents(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed == True:
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    self.bg = PANE_BG_LITE
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.bg = PANE_BG_LITE
            elif self.bg == PANE_BG_LITE:
                self.bg = PANE_BG_DARK
                

    def update(self):
        if self.pressed and self.bg != PANE_BG_DARK:
            self.bg = PANE_BG_DARK
        self.surf = self.font.render(self.title,False,self.fg,self.bg)