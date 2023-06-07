import pygame as pg
import os

from config import *
from Monster import Monster 
from MonsterData import MonsterData

class MonsterBankPane(pg.sprite.Sprite):
    def __init__(self):
        super(MonsterBankPane, self).__init__()

        self.font = pg.font.Font('grand9k.ttf',14)

        self.border = pg.sprite.Sprite()
        self.border.surf = pg.Surface((270, SCREEN_H - PAD*2 - 24),)
        self.border.surf.fill(SCREEN_BG)
        self.border.rect = self.border.surf.get_rect().move(16, 24 + PAD)
        pg.draw.rect(self.border.surf, PANE_BG_LITE,
                    (0,0,self.border.rect.w, self.border.rect.h), 
                    border_radius=4)
        pg.draw.rect(self.border.surf, FG_WHITE,
                    (0,0,self.border.rect.w, self.border.rect.h), 
                    border_radius=4, width=2)

        self.surf = pg.Surface((266, SCREEN_H - PAD*2 - 24 - 24 - 2))
        self.surf.fill(PANE_BG_DARK)
        self.rect = self.surf.get_rect().move(16 + 2, 24 + 24 + PAD)
        
        self.btn = pg.sprite.Sprite()
        self.btn.surf = self.font.render(
            "Stage", False, FG_ORANGE, PANE_BG_LITE)
        self.btn.rect = self.btn.surf.get_rect().move(
            self.border.rect.left + 6, self.border.rect.top + 3)

        self.stage_sel = list(STAGE_ORDER.keys())[0]

        self.moused_over = "" 
        self.mon_indicator = self.font.render(
            self.moused_over, False, FG_ORANGE, (25,25,25))

        self.keys_enabled = True

    def load_sprites(self, screen):
        self.mons = {}
        x = {}
        y = {}
        cols = 6
        last_dir = ""
        for r,d,f in os.walk("sprites/"):
            for dir in d:
                self.mons[dir] = pg.sprite.LayeredUpdates()
                x[dir] = 0
                y[dir] = 0
            for file in f:
                if 'png' not in file:
                    continue
                filename = os.path.join(r,file).replace('\\','/')
                fdir = filename.split('/')[1]
                if fdir != last_dir:
                    last_dir = fdir
                    load_msg = self.font.render(f"Loading sprites: {last_dir}",
                                                False,FG_ORANGE,SCREEN_BG)
                    screen.fill(SCREEN_BG)
                    screen.blit(load_msg,
                                (SCREEN_W/2 - load_msg.get_width()/2,
                                SCREEN_H/2 - load_msg.get_height()/2))
                    pg.display.flip()

                data = MonsterData(
                    filepath = filename,
                    coords = ( 
                    self.rect[0] + PAD + x[fdir],
                    self.rect[1] + PAD + y[fdir]
                    )
                )
                self.mons[fdir].add(Monster(data))
                x[fdir] = (x[fdir] + 40) % (cols * 40)
                if x[fdir] == 0:
                    y[fdir] += 40

    def change_stage(self, dir):
        stages = list(STAGE_ORDER.keys())
        self.stage_sel = stages[
            (stages.index(self.stage_sel) + dir) % len(stages)]

    def update(self, event_list):
        for event in event_list:
            if event.type == CMD_ACTIVE:
                self.keys_enabled = False
            elif event.type == CMD_INACTIVE:
                self.keys_enabled = True

            elif event.type == KEYDOWN and self.keys_enabled:
                if event.key == K_w:
                    self.change_stage(-1)
                elif event.key == K_s:
                    self.change_stage(1)
                elif event.key in STAGE_KEYS.keys():
                    self.stage_sel = STAGE_KEYS[event.key]

            elif event.type == pg.MOUSEWHEEL:
                mouse_pos = pg.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.surf.scroll(0,event.y*25)
                    for mon in self.mons[self.stage_sel]:
                        mon.rect.y += 25*event.y
                        mon.data.coords = mon.rect.topleft

        self.btn.surf = self.font.render(
            self.stage_sel, False, FG_ORANGE,PANE_BG_LITE)

        mouse_pos = pg.mouse.get_pos()
        self.moused_over = ""
        for mon in self.mons[self.stage_sel]:
            if not mon.rect.collidepoint(mouse_pos):
                continue
            if not mon.rect.colliderect(self.rect):
                continue
            if self.moused_over != mon.data.name:
                mon.set_border(FG_WHITE)
                self.moused_over = mon.data.name
                self.mon_indicator = self.font.render(
                    mon.data.name, False, FG_ORANGE, (25,25,25))
            elif mon.border_color != (200,200,200):
                mon.set_border((200,200,200))

    def draw(self, screen):
        self.surf.fill(PANE_BG_DARK)
        self.btn.surf = self.font.render(
            self.stage_sel, False, FG_ORANGE, PANE_BG_LITE)
        for mon in self.mons[self.stage_sel]:
            mon.update()
            mon_x = mon.rect.x - self.rect.left
            mon_y = mon.rect.y - self.rect.top
            self.surf.blit(mon.surf, (mon_x, mon_y, mon.rect.w, mon.rect.h))
            screen.blit(self.border.surf, self.border.rect)
            screen.blit(self.surf, self.rect)
            screen.blit(self.btn.surf, self.btn.rect)
        if self.moused_over:
            indicator_x = pg.mouse.get_pos()[0] + 12
            indicator_y = pg.mouse.get_pos()[1] - 12
            screen.blit(self.mon_indicator, (indicator_x, indicator_y))