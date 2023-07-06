#
# Evolution tree builder for Tyrannomon
#

import pygame as pg
from PIL import Image
import os
import copy

from Monster import Monster
from MonsterData import MonsterData
from SandboxPane import SandboxPane
from BackgroundPane import BackgroundPane
from PreviewPane import PreviewPane
from MicroConsole import MicroConsole
from MonsterBankPane import MonsterBankPane
from InfoLayer import InfoLayer
from SpriteModder import SpriteModder
from config import *

def run_gui():
    pg.init()

    pg.display.set_caption("Digitizer")
    pygame_icon = pg.image.load('gfx/icon.png')
    pg.display.set_icon(pygame_icon)

    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    
    clock = pg.time.Clock()

    running = True

    console = MicroConsole()
    bg_pane = BackgroundPane()
    preview_pane = PreviewPane()
    sandbox_pane = SandboxPane()
    bank_pane = MonsterBankPane()
    info_layer = InfoLayer()
    sprite_modder = SpriteModder()

    panes = pg.sprite.LayeredUpdates()
    panes.add(console)
    panes.add(bg_pane)
    panes.add(preview_pane)
    panes.add(bank_pane)
    panes.add(sandbox_pane)
    panes.add(info_layer)

    bank_pane.load_sprites(screen)

    while running:
        clock.tick(60)

        event_list = pg.event.get()
        
        for event in event_list:
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in bank_pane.mons[bank_pane.stage_sel]:
                        if mon.rect.collidepoint(event.pos):
                            data_copy = copy.deepcopy(mon.data)
                            sandbox_pane.add_mon(Monster(data_copy))

            elif event.type == CMD_CONVERT_SPRITES:
                sprite_modder.convert_sprites(event.path)
            
            elif event.type == CMD_RELOAD_SPRITES:
                bank_pane.load_sprites(screen)

        #Draw
        screen.fill(SCREEN_BG)

        sprite_modder.update(event_list)

        for pane in panes:
            pane.update(event_list)
            pane.draw(screen)

        pg.display.flip()

def main():
    run_gui()

if __name__ == '__main__':
    main()