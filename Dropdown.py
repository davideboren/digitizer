import pygame as pg
from config import *

class Dropdown(pg.sprite.Sprite):
    def __init__(self,title):

        super(Dropdown,self).__init__()

        self.title = title
        self.font = pg.font.Font("grand9k.ttf",14)
        self.fg = FG_WHITE
        self.bg = PANE_BG_COLOR
        self.surf = self.font.render(title,False,self.fg,self.bg)
        self.rect = self.surf.get_rect()
    
    def handleEvents(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.bg = PANE_BG_COLOR
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.bg == PANE_BG_COLOR:
                self.bg = PANE_BG_COLOR2
        if event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.bg = PANE_BG_COLOR2
            elif self.bg == PANE_BG_COLOR2:
                self.bg = PANE_BG_COLOR

    def update(self):
        self.surf = self.font.render(self.title,False,self.fg,self.bg)