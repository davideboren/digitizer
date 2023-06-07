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
from config import *

def run_gui():
    pg.init()

    pg.display.set_caption("Digitizer")
    pygame_icon = pg.image.load('icon.png')
    pg.display.set_icon(pygame_icon)

    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    
    clock = pg.time.Clock()

    running = True

    console = MicroConsole()
    bg_pane = BackgroundPane()
    preview_pane = PreviewPane()
    sandbox_pane = SandboxPane()
    bank_pane = MonsterBankPane()

    panes = pg.sprite.LayeredUpdates()
    panes.add(console)
    panes.add(bg_pane)
    panes.add(preview_pane)
    panes.add(bank_pane)
    panes.add(sandbox_pane)

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
                convert_sprites()

        #Draw
        screen.fill(SCREEN_BG)

        for pane in panes:
            pane.update(event_list)
            pane.draw(screen)

        pg.display.flip()

def convert_sprites():
    if not os.path.exists("out/sprites"):
        os.mkdir("out/sprites")
    for r, d, f in os.walk("sprites"):
        for dir in d:
            if not os.path.exists(os.path.join("out/sprites",dir)):
                os.mkdir(os.path.join("out/sprites",dir))
        for file in f:
            if "png" in file:
                filepath = os.path.join(r,file)
                output = os.path.join("out",filepath)
                
                print("Converting ",filepath)
                
                spr = Image.open(filepath)
                
                sprW, sprH = spr.size
                for h in range(0,sprH):
                    for w in range(0,sprW):
                        if(spr.getpixel((w,h)) == (255,0,255,255)):
                            print("WARNING: Found #FF00FF pixel")
                        if(spr.getpixel((w,h))[3] == 0):
                            spr.putpixel((w,h),(255,0,255,255))
                
                spr = spr.convert("RGB")
                spr.save(output.replace("png","bmp"))
        print("Done!")

def main():
    run_gui()

if __name__ == '__main__':
    main()