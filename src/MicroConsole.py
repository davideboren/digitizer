import pygame as pg
import glob

from config import *

class MicroConsole(pg.sprite.Sprite):

    def __init__(self):
        super(MicroConsole, self).__init__()

        self.commands = {
            # cmd : applicable filename pattern
            'save' : '.pkl',
            'load' : '.pkl',
            'export' : '',
            'new_tab' : '',
            'convert_sprites' : '',
            'reload_sprites' : '',
            'set_palette' : '.gpl'
        }

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
        self.prefix = ""
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
        pg.event.post(pg.event.Event(CMD_ACTIVE))

    def make_inactive(self):
        self.font_color = FG_LITE_GRAY
        self.active = False
        pg.event.post(pg.event.Event(CMD_INACTIVE))

    def tab_complete(self):
        if not self.tabbing:
            self.prefix = ''
            self.tab_options = []
            self.tab_cmd = self.input.lstrip(' ').split(' ')
            self.tabbing = True
        if len(self.tab_cmd) == 1:
            for c in list(self.commands.keys()):
                if c.startswith(self.tab_cmd[0]):
                    if c not in self.tab_options:
                        self.tab_options.append(c)
            if not self.tab_options:
                self.prefix = self.tab_cmd[0]
        elif len(self.tab_cmd) == 2:
            self.prefix = self.tab_cmd[0] + ' '
            if self.tab_cmd[0] in self.commands:
                files = glob.glob(self.tab_cmd[1] + '*' )
                filetype = self.commands[self.tab_cmd[0]]
                for f in files:
                    if not f.endswith(filetype):
                        continue
                    if f.startswith(self.tab_cmd[1]):
                        if f not in self.tab_options:
                            self.tab_options.append(f)

        if self.tab_options:
            target = self.tab_options[self.tab_idx]
            self.tab_idx = (self.tab_idx + 1) % len(self.tab_options)
        else:
            target = ''
        self.input = self.prefix + target

    def send_cmd(self):
        if self.input.startswith("save"):
            if len(self.input.split(" ")) > 1:
                savefile = self.input.split(" ")[1]
            else:
                savefile = ""
            pg.event.post(pg.event.Event(CMD_SAVE,
                                         {"filename" : savefile}))
        elif self.input.startswith("load"):
            if len(self.input.split(' ')) == 1:
                loadfile = ''
            else:
                loadfile = self.input.split(" ")[1]
            pg.event.post(pg.event.Event(CMD_LOAD,
                                         {"filename" : loadfile}))
        elif self.input.startswith("export"):
            pg.event.post(pg.event.Event(CMD_EXPORT))
        elif self.input.startswith("new_tab"):
            pg.event.post(pg.event.Event(CMD_NEW_TAB))
        elif self.input.startswith("convert_sprites"):
            if len(self.input.split(" ")) > 1:
                path = self.input.split(" ")[1]
            else:
                path = ""
            pg.event.post(pg.event.Event(CMD_CONVERT_SPRITES,
                          {"path" : path}))
        elif self.input.startswith("reload_sprites"):
            pg.event.post(pg.event.Event(CMD_RELOAD_SPRITES))
        elif self.input.startswith("set_palette"):
            if len(self.input.split(" ")) > 1:
                path = self.input.split(" ")[1]
            else:
                path = "palettes/aap-64.gpl"
            pg.event.post(pg.event.Event(CMD_SET_PALETTE,
                          {"path" : path}))
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
                    self.tab_complete()
                else:
                    self.input += event.unicode

        #visuals
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