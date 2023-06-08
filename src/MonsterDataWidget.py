import pygame as pg

from MonsterData import MonsterData
from config import *

class MonsterDataWidget(pg.sprite.Sprite):
    def __init__(self):
        super(MonsterDataWidget, self).__init__()

        self.font = pg.font.Font('grand9k.ttf',14)
        self.anchor = (0,0)
        self.data = MonsterData()

        self.datapoints = []

        self.ignored_fields = [
            'filepath',
            'stage',
            'bg',
            'evos',
            'tab',
            'coords'
        ]

    def set_mon(self, data):
        self.data = data
        self.datapoints = []
        idx = 1
        for key in reversed(list(self.data.__dict__.keys())):
            if key in self.ignored_fields:
                continue
            text = f"{key}: {self.data.__dict__[key]}"
            spr = pg.sprite.Sprite()
            spr.surf = self.font.render(text, False, FG_WHITE)
            spr.rect = spr.surf.get_rect()
            spr_x = self.anchor[0] - spr.rect.w
            spr_y = self.anchor[1] - spr.rect.h*idx
            spr.rect.move_ip(spr_x, spr_y)
            self.datapoints.append(spr)
            idx += 1

    def update(self, event_list):
        return
    
    def draw(self, screen):
        for d in self.datapoints:
            screen.blit(d.surf, d.rect)