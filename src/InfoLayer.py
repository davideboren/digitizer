import pygame as pg

from config import *

class InfoLayer(pg.sprite.Sprite):
    def __init__(self):
        super(InfoLayer, self).__init__()

        self.font = pg.font.Font('grand9k.ttf',14)
        self.nameplate_txt = ""
        self.nameplate_enabled = False

    def update(self, event_list):
        for event in event_list:
            if event.type == INFO_NAMEPLATE_OFF:
                self.nameplate_enabled = False
                print("NAME OFF")
            elif event.type == INFO_NAMEPLATE_ON:
                print("NAME ON")
                self.nameplate_txt = event.name
                self.nameplate_enabled = True

    def draw(self, screen):
        if self.nameplate_enabled:
            np_x = pg.mouse.get_pos()[0] + 12
            np_y = pg.mouse.get_pos()[1] - 12
            nameplate = self.font.render(self.nameplate_txt,
                                         False, FG_ORANGE, PANE_BG_LITE)
            screen.blit(nameplate, (np_x, np_y))
