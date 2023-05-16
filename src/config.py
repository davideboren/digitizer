import pygame as pg
from pygame.locals import (
    K_ESCAPE,
    K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,
    K_w,K_a,K_c,K_e,K_s,K_d,K_o,K_l,
    KEYDOWN,
    QUIT
)

#Window
SCREEN_W = 1280
SCREEN_H = 720
PAD = 16

BG_PANE_W = 200
BG_PANE_H = SCREEN_H - PAD*3 - 24 - 200

PREVIEW_PANE_W = 200
PREVIEW_PANE_H = 200

#Colors
SCREEN_BG = (24,24,48)
MENU_BG_COLOR = (90,70,90)
PANE_BG_DARK = (40,40,40)
PANE_BG_LITE = (60,60,60)
FG_WHITE = (255,255,255,255)
FG_ORANGE = (250,170,0)
FG_GREEN = (50,255,0)

SPRITE_DIR = "sprites/"
STAGE_ORDER = {
    "digitama": 0,
    "baby":     1,
    "baby_ii":  2,
    "child":    3,
    "adult":    4,
    "perfect":  5,
    "ultimate": 6,
    "armor":    9
}
STAGE_KEYS = {
    K_1 : "digitama",
    K_2 : "baby",
    K_3 : "baby_ii",
    K_4 : "child",
    K_5 : "adult",
    K_6 : "perfect",
    K_7 : "ultimate",
    K_0 : "armor",
}

MON_SELECT = pg.USEREVENT + 1