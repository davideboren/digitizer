import pygame as pg
from config import *


class Sandbox(pg.sprite.Sprite):

    def __init__(self):
        super(Sandbox, self).__init__()

        self.surf = pg.Surface((736, SCREEN_H - PAD*2 - 24))
        self.rect = self.surf.get_rect().move(284 + PAD, 24 + PAD)
        self.offset_x = 0
        self.offset_y = 0

        self.tab = 0
        self.mons = []
        self.mons.append(pg.sprite.LayeredUpdates())

        self.mon_sel = None

        #Pane background
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

    def remove_mon(self, mon):
        self.mons[self.tab].remove(mon)

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
    
    def update(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_d:
                    self.tab = (self.tab + 1) % len(self.mons)
                elif event.key == K_a:
                    self.tab = (self.tab - 1) % len(self.mons)
                
            #Drag and Drop
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in self.get_mons():
                        if mon.rect.collidepoint(event.pos):
                            mon.set_border((50,255,0))
                            mon.dragging = True
                            mouse_x, mouse_y = event.pos
                            self.offset_x = mon.rect.x - mouse_x
                            self.offset_y = mon.rect.y - mouse_y
                elif event.button == 2:
                    for mon in self.get_mons():
                        if mon.rect.collidepoint(event.pos):
                            if mon == self.mon_sel:
                                self.mon_sel = None
                            self.remove_mon(mon)
                elif event.button == 3:
                    for mon in self.get_mons():
                        if mon.rect.collidepoint(event.pos):
                            if self.mon_sel == None:
                                self.mon_sel = mon
                                break
                            elif mon in self.mon_sel.evos:
                                self.mon_sel.evos.remove(mon)
                            elif self.mon_sel in mon.evos:
                                mon.evos.remove(self.mon_sel)
                            else:
                                if mon.stage != self.mon_sel.stage:
                                    if STAGE_ORDER[self.mon_sel.stage] < STAGE_ORDER[mon.stage]:
                                        self.mon_sel.evos.append(mon)
                                    else:
                                        mon.evos.append(self.mon_sel)
                            self.mon_sel = None
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    for mon in self.get_mons():
                        mon.dragging = False
                        if not mon.rect.colliderect(self.rect):
                            self.remove_mon(mon)
            elif event.type == pg.MOUSEMOTION:
                for mon in self.get_mons():
                    if mon.dragging:
                        if not mon.rect.colliderect(self.rect):
                            if mon.surf.get_alpha() != 125:
                                mon.surf.set_alpha(125)
                        elif mon.surf.get_alpha() == 125:
                            mon.surf.set_alpha(255)
                        mouse_x, mouse_y = event.pos
                        mon.rect.x = mouse_x + self.offset_x
                        mon.rect.y = mouse_y + self.offset_y

    def draw(self, surf):
        surf.blit(self.surf, self.rect)