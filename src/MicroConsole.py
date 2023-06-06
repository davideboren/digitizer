import pygame as pg
import glob

from config import *

class MicroConsole(pg.sprite.Sprite):

    def __init__(self):
        super(MicroConsole, self).__init__()

        self.surf = pg.Surface((SCREEN_W, 24))
        self.rect = self.surf.get_rect()
        self.surf.fill(CONSOLE_BG_COLOR)
        self.font = pg.font.Font('grand9k.ttf',7)
        self.font_color = FG_LITE_GRAY

        self.prompt = "# "
        self.cur = "_"
        self.input = ""
        self.output = ""
        self.tabbing = False
        self.tab_cmd = []
        self.tab_options = []
        self.tab_idx = 0

        self.input_zone = self.font.render(self.prompt + self.input + self.cur, 
                                          False, self.font_color, CONSOLE_BG_COLOR)
        self.surf.blit(pg.transform.scale(self.input_zone,(self.input_zone.get_width()*2,
                                                           self.input_zone.get_height()*2)), (2, 0))

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
        elif self.input.startswith("load "):
            loadfile = self.input.split(" ")[1]
            pg.event.post(pg.event.Event(CMD_LOAD,
                                         {"filename" : loadfile}))
        elif self.input.startswith("export"):
            pg.event.post(pg.event.Event(CMD_EXPORT))
        elif self.input.startswith("new_tab"):
            pg.event.post(pg.event.Event(CMD_NEW_TAB))
        else:
            uc_msg("Unrecognized command")


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
            elif self.active and event.type == pg.KEYDOWN:
                if event.key != K_TAB:
                    self.tabbing = False
                    self.tab_idx = 0
                if event.key == K_BACKSPACE:
                    self.input = self.input[:-1]
                elif event.key == K_RETURN:
                    self.send_cmd()
                    self.make_inactive()
                elif event.key == K_TAB:
                    if not self.tabbing:
                        self.tab_cmd = self.input.split(' ')
                        self.tabbing = True
                    if self.tab_cmd[0] == "":
                        self.tab_options = ['save ', 'load ', 'new_tab', 'export']
                        self.input = self.tab_options[self.tab_idx]
                    elif self.tab_cmd[0] == "load":
                        prefix = ""
                        if len(self.tab_cmd) > 1:
                            prefix = self.tab_cmd[1]
                        self.tab_options = glob.glob(prefix + "*.pkl") 
                        if self.tab_options:
                            file = self.tab_options[self.tab_idx]
                            self.input = "load " + file
                    if len(self.tab_options):
                        self.tab_idx = (self.tab_idx + 1) % len(self.tab_options)
                else:
                    self.input += event.unicode

        self.ticks += 1
        if self.ticks >= 30:
            if self.active:
                self.cur = " " if self.cur == "_" else "_"
            self.ticks = 0

        self.surf.fill(CONSOLE_BG_COLOR)
        self.input_zone = self.font.render(self.prompt + self.input + self.cur,
                                          False, self.font_color, CONSOLE_BG_COLOR)
        iz_w = self.input_zone.get_width()*2
        iz_h = self.input_zone.get_height()*2
        self.input_zone = pg.transform.scale(self.input_zone, (iz_w, iz_h))
        self.surf.blit(self.input_zone, (2, 0))

        self.output_zone = self.font.render(self.output, False, 
                                            self.font_color, CONSOLE_BG_COLOR)
        oz_w = self.output_zone.get_width()*2
        oz_h = self.output_zone.get_height()*2
        self.output_zone = pg.transform.scale(self.output_zone, (oz_w, oz_h))
        self.output_rect = self.output_zone.get_rect()
        self.output_rect.right = SCREEN_W - 2
        self.surf.blit(self.output_zone, self.output_rect)

    def draw(self, surf):
        surf.blit(self.surf, self.rect)