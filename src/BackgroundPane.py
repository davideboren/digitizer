import pygame as pg
import os

from config import *

class BackgroundPane(pg.sprite.Sprite):

    def __init__(self):
        super(BackgroundPane, self).__init__()

        self.border = pg.sprite.Sprite()
        self.border.surf = pg.Surface((BG_PANE_W, BG_PANE_H))
        self.border.surf.fill(SCREEN_BG)
        self.border.rect = self.border.surf.get_rect().move(1036 + PAD, 24 + PAD)
        pg.draw.rect(self.border.surf, FG_WHITE,
                    (0,0,self.border.rect.w, self.border.rect.h), 
                    border_radius=4, width=2)

        self.surf = pg.Surface((BG_PANE_W - 4, BG_PANE_H - 4))
        self.rect = self.surf.get_rect().move(1038 + PAD, 26 + PAD)

        self.bgs = {}
        self.bg_sel = None
        self.bg_filepath = None

        x_margin = round(BG_PANE_W - 128 - 4)/3
        bg_x = x_margin
        bg_y = PAD

        for r,d,f in os.walk("bg/"):
            for file in f:
                if 'bmp' in file:
                    filepath = os.path.join(r,file).replace('\\','/')
                    bg = pg.sprite.Sprite()
                    bg.img = pg.image.load(filepath)
                    bg.surf = pg.Surface((64+2, 64+2))
                    bg.surf.fill(FG_WHITE)
                    bg.rect = pg.Rect(1, 1, 64+2, 64+2)
                    bg.surf.blit(bg.img, bg.rect)
                    bg.rect.move_ip(bg_x,bg_y)
                    self.bgs[bg] = filepath
                    if bg_x == x_margin:
                        bg_x = 64 + x_margin*2
                    else:
                        bg_x = x_margin
                        bg_y += 64 + PAD*2
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

    def draw(self, screen):
        screen.blit(self.border.surf, self.border.rect)
        self.surf.fill(PANE_BG_DARK)
        for bg in self.bgs:
            self.surf.blit(bg.surf, bg.rect)
        screen.blit(self.surf, self.rect)
