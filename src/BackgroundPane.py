import pygame as pg
import os

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

        self.bgs = {}
        self.bg_sel = None
        self.bg_filepath = None
        bg_x = BG_PANE_W/2 - 64
        bg_y = PAD

        for r,d,f in os.walk("bg/"):
            for file in f:
                if 'png' in file or 'bmp' in file:
                    filepath = os.path.join(r,file).replace('\\','/')
                    bg = pg.sprite.Sprite()
                    bg.img = pg.image.load(filepath)
                    bg.surf = pg.Surface((128+2,128+2))
                    bg.surf.fill(FG_WHITE)
                    bg.rect = pg.Rect(1,1,128+2,128+2)
                    bg.surf.blit(pg.transform.scale(bg.img,(128,128)),bg.rect)
                    bg.rect.move_ip(bg_x,bg_y)
                    self.bgs[bg] = filepath
                    bg_y += 128 + PAD*2
                    if self.bg_sel == None:
                        self.bg_sel = bg
                        self.bg_filepath = filepath 

    def update(self, event_list):
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for bg in self.bgs:
                    adj_pos = (event.pos[0] - self.rect.left,
                               event.pos[1] - self.rect.top)
                    if (bg.rect.collidepoint(adj_pos)
                        and self.rect.collidepoint(event.pos)):
                        self.bg_sel = bg
                        self.bg_filepath = self.bgs[bg]
                        pg.event.post(pg.event.Event(
                            BG_SELECT, {"filepath":self.bg_filepath}))
            elif event.type == pg.MOUSEWHEEL:
                mouse_pos = pg.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.surf.scroll(0, event.y*25)
                    for bg in self.bgs:
                        bg.rect.y += 25*event.y

    def draw(self, surf):
        pg.draw.rect(self.surf, PANE_BG_DARK,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4)
        pg.draw.rect(self.surf, FG_WHITE,
                    (0,0,self.rect.w, self.rect.h), 
                    border_radius=4, width = 2)

        for bg in self.bgs:
            self.surf.blit(bg.surf, bg.rect)

        surf.blit(self.surf, self.rect)
