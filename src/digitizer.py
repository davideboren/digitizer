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
                convert_sprites(event.path)

        #Draw
        screen.fill(SCREEN_BG)

        for pane in panes:
            pane.update(event_list)
            pane.draw(screen)

        pg.display.flip()

def convert_sprites(path):
    if path == "":
        path = "sprites"
    out_path = f"out/{path}"
    if not os.path.exists("out"):
        os.mkdir("out")
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    for r, d, f in os.walk(path):
        for dir in d:
            if not os.path.exists(os.path.join(out_path,dir)):
                os.mkdir(os.path.join(out_path,dir))
        for file in f:
            if "png" in file or "bmp" in file:
                filepath = os.path.join(r,file)
                output = os.path.join("out",filepath)
                
                print("Converting ",filepath)
                
                spr = Image.open(filepath)
                
                if "png" in file:
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