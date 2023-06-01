import pygame as pg
import glob

from config import *

class MicroConsole(pg.sprite.Sprite):

    def __init__(self):
        super(MicroConsole, self).__init__()

        self.surf = pg.Surface((SCREEN_W, 24))
        self.rect = self.surf.get_rect()
        self.surf.fill(CONSOLE_BG_COLOR)
        self.font = pg.font.Font('grand9k.ttf',14)
        self.font_color = FG_LITE_GRAY

        self.prompt = "# "
        self.cur = "_"
        self.input = ""
        self.output = ""
        self.auto_idx = 0

        self.input_zone = self.font.render(self.prompt + self.input + self.cur, 
                                          False, self.font_color, CONSOLE_BG_COLOR)
        self.surf.blit(self.input_zone, (2, 0))

        self.ticks = 0
        self.active = False

    def make_active(self):
        self.font_color = FG_WHITE
        self.active = True

    def make_inactive(self):
        self.font_color = FG_LITE_GRAY
        self.active = False

    def send_cmd(self):
        if self.input.startswith("save "):
            savefile = self.input.split(" ")[1]
            pg.event.post(pg.event.Event(CMD_SAVE,
                                         {"filename" : savefile}))
        if self.input.startswith("load "):
            loadfile = self.input.split(" ")[1]
            pg.event.post(pg.event.Event(CMD_LOAD,
                                         {"filename" : loadfile}))
        if self.input == ("export"):
            pg.event.post(pg.event.Event(CMD_EXPORT))


        self.input = ""

    def update(self, event_list):
        for event in event_list:
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                if self.rect.collidepoint(pg.mouse.get_pos()):
                    self.make_active()
                elif self.active:
                    self.make_inactive()
            elif event.type == pg.KEYDOWN and event.key == K_BACKQUOTE:
                if not self.active:
                    self.make_active()
                else:
                    self.make_inactive()
            elif event.type == pg.KEYDOWN and event.key == K_ESCAPE:
                self.make_inactive()
            elif event.type == CMD_MSG:
                self.output = event.msg
            elif self.active:
                if event.type == pg.KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.input = self.input[:-1]
                    elif event.key == K_RETURN:
                        self.send_cmd()
                    elif event.key == K_TAB:
                        if self.input.startswith("load "):
                            saves = glob.glob("*.pkl") 
                            if saves:
                                file = saves[self.auto_idx]
                                self.input = "load " + file
                                self.auto_idx = (self.auto_idx + 1) % len(saves)
                    else:
                        self.input += event.unicode

        self.ticks += 1
        if self.ticks >= 30:
            if self.active:
                self.cur = " " if self.cur == "_" else "_"
            self.ticks = 0

        self.input_zone = self.font.render(self.prompt + self.input + self.cur,
                                          False, self.font_color, CONSOLE_BG_COLOR)
        self.output_zone = self.font.render(self.output, False, 
                                            self.font_color, CONSOLE_BG_COLOR)
        self.output_rect = self.output_zone.get_rect()
        self.output_rect.right = SCREEN_W
        self.surf.fill(CONSOLE_BG_COLOR)
        self.surf.blit(self.input_zone, (2, 0))
        self.surf.blit(self.output_zone, self.output_rect)

    def draw(self, surf):
        surf.blit(self.surf, self.rect)