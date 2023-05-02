#
# Converts Transparent .png spritesheets to 24-bit BMPs
# Any transparent pixels are changed to #FF00FF
#

import pygame as pg
from PIL import Image
import os
import re
import dataclasses

from Monster import Monster, MonsterData
from Dropdown import Dropdown
from Sandbox import Sandbox
from config import *


def run_gui():

    pg.init()

    pg.display.set_caption("Digitizer")
    pygame_icon = pg.image.load('icon.png')
    pg.display.set_icon(pygame_icon)
    mon_font = pg.font.Font('grand9k.ttf',14)

    screen = pg.display.set_mode((SCREEN_W,SCREEN_H))
    
    clock = pg.time.Clock()

    running = True

    # Background Panes
    panes = pg.sprite.LayeredUpdates()

    mon_pane_border = pg.sprite.Sprite()
    mon_pane_border.surf = pg.Surface((270, SCREEN_H - PAD*2 - 24),)
    mon_pane_border.surf.fill(SCREEN_BG)
    mon_pane_border.rect = mon_pane_border.surf.get_rect().move(16,24 + PAD)
    pg.draw.rect(mon_pane_border.surf, PANE_BG_LITE,
                 (0,0,mon_pane_border.rect.w, mon_pane_border.rect.h), 
                 border_radius=4)
    pg.draw.rect(mon_pane_border.surf, FG_WHITE,
                 (0,0,mon_pane_border.rect.w, mon_pane_border.rect.h), 
                 border_radius=4, width=2)
    mon_pane = pg.sprite.Sprite()
    mon_pane.surf = pg.Surface((266, SCREEN_H - PAD*2 - 24 - 24 - 2),)
    mon_pane.surf.fill(PANE_BG_DARK)
    mon_pane.rect = mon_pane.surf.get_rect().move(16 + 2, 24 + 24 + PAD)
    
    mon_pane_btn = pg.sprite.Sprite()
    mon_pane_btn.surf = mon_font.render("Stage",False,FG_ORANGE,PANE_BG_LITE)
    mon_pane_btn.rect = mon_pane_btn.surf.get_rect().move(
        mon_pane_border.rect.left + 6,mon_pane_border.rect.top + 3)
    
    sandbox = Sandbox()

    bg_pane = pg.sprite.Sprite()
    bg_pane.surf = pg.Surface((BG_PANE_W,BG_PANE_H))
    bg_pane.rect = bg_pane.surf.get_rect().move(
        sandbox.rect.right + PAD, 24 + PAD)
    pg.draw.rect(bg_pane.surf, PANE_BG_DARK,
                 (0,0,bg_pane.rect.w, bg_pane.rect.h), 
                 border_radius=4)
    pg.draw.rect(bg_pane.surf, FG_WHITE,
                 (0,0,bg_pane.rect.w, bg_pane.rect.h), 
                 border_radius=4, width = 2)

    preview_pane = pg.sprite.Sprite()
    preview_pane.surf = pg.Surface((PREVIEW_PANE_W,PREVIEW_PANE_H))
    preview_pane.rect = preview_pane.surf.get_rect().move(
        sandbox.rect.right + PAD, SCREEN_H - PAD - 200)
    pg.draw.rect(preview_pane.surf, PANE_BG_DARK,
                 (0,0,preview_pane.rect.w, preview_pane.rect.h), 
                 border_radius=4)
    pg.draw.rect(preview_pane.surf, FG_WHITE,
                 (0,0,preview_pane.rect.w, preview_pane.rect.h), 
                 border_radius=4, width = 2)

    panes.add(mon_pane_border)
    panes.add(mon_pane)
    panes.add(mon_pane_btn)
    panes.add(bg_pane)
    panes.add(preview_pane)
    
    # Monsters
    mons = {}
    x = {}
    y = {}
    cols = 6
    last_dir = ""
    for r,d,f in os.walk("sprites/"):
        for dir in d:
            mons[dir] = pg.sprite.LayeredUpdates()
            x[dir] = 0
            y[dir] = 0
        for file in f:
            if 'png' in file:
                filename = os.path.join(r,file).replace('\\','/')
                fdir = filename.split('/')[1]
                if fdir != last_dir:
                    last_dir = fdir
                    load_msg = mon_font.render(f"Loading sprites: {last_dir}",False,FG_ORANGE,SCREEN_BG)
                    screen.fill(SCREEN_BG)
                    screen.blit(load_msg,
                                (SCREEN_W/2 - load_msg.get_width()/2,
                                 SCREEN_H/2 - load_msg.get_height()/2))
                    pg.display.flip()

                data = MonsterData(
                    filename,
                    filename.split('/')[-1].split('.')[0],
                    filename.split('/')[-2],
                    "walk",
                    "",
                    [],
                    -1,
                    (mon_pane.rect[0] + PAD + x[fdir],
                     mon_pane.rect[1] + PAD + y[fdir])
                )
                mons[fdir].add(Monster(data))
                x[fdir] = (x[fdir] + 40) % (cols * 40)
                if x[fdir] == 0:
                    y[fdir] += 40

    bgs = pg.sprite.LayeredUpdates()
    bg_sel = None

    for r,d,f in os.walk("bg/"):
        for file in f:
            if 'png' in file:
                filepath = os.path.join(r,file).replace('\\','/')
                bg = pg.sprite.Sprite()
                bg.img = pg.image.load(filepath)
                bg.surf = pg.Surface((128+2,128+2))
                bg.surf.fill(FG_WHITE)
                bg.rect = pg.Rect(1,1,128+2,128+2)
                bg.surf.blit(pg.transform.scale(bg.img,(128,128)),bg.rect)
                bg.rect.move_ip(BG_PANE_W/2 - bg.rect.w/2, PAD)
                bgs.add(bg)
                bg_sel = bg

    #Info 
    info = pg.sprite.LayeredUpdates()

    menu_bar = pg.sprite.Sprite()
    menu_bar.surf = pg.Surface((SCREEN_W, 24))
    menu_bar.rect = menu_bar.surf.get_rect()
    menu_bar.surf.fill(MENU_BG_COLOR)
    pg.draw.line(menu_bar.surf,(5,15,35),
                 (0,menu_bar.rect[3] - 2),
                 (SCREEN_W,menu_bar.rect[3] - 2),
                 width = 2)

    menu_bar_file = Dropdown(
    [PANE_BG_DARK, PANE_BG_LITE],
    [PANE_BG_DARK, PANE_BG_LITE],
    0, 0, 40, 22, 
    "File", ["New", "Open", "Exit"])

    info.add(menu_bar)

    stage_sel = list(STAGE_ORDER.keys())[0]

    moused_over = "" 
    mon_indicator = mon_font.render(moused_over,False,FG_ORANGE,(25,25,25))

    while running:
        
        clock.tick(60)

        event_list = pg.event.get()

        menu_bar_file.update(event_list)
        
        for event in event_list:

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key in STAGE_KEYS.keys():
                    stage_sel = STAGE_KEYS[event.key]
                elif event.key == K_w:
                    stages = list(STAGE_ORDER.keys())
                    stage_sel = stages[(stages.index(stage_sel)-1)%len(stages)]
                elif event.key == K_s:
                    stages = list(STAGE_ORDER.keys())
                    stage_sel = stages[(stages.index(stage_sel)+1)%len(stages)]
            elif event.type == QUIT:
                running = False
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in mons[stage_sel]:
                        if mon.rect.collidepoint(event.pos):
                            data_copy = dataclasses.replace(mon.data)
                            sandbox.add_mon(Monster(data_copy))
            elif event.type == pg.MOUSEWHEEL:
                mouse_pos = pg.mouse.get_pos()
                if mon_pane.rect.collidepoint(mouse_pos):
                    mon_pane.surf.scroll(0,event.y*25)
                    for mon in mons[stage_sel]:
                        mon.rect.y += 25*event.y

        mouse_pos = pg.mouse.get_pos()
        moused_over = ""
        for mon in mons[stage_sel]:
            if mon.rect.collidepoint(mouse_pos) and mon.rect.colliderect(mon_pane.rect) and moused_over != mon.data.name:
                mon.set_border(FG_WHITE)
                moused_over = mon.data.name
                mon_indicator = mon_font.render(mon.data.name,False,FG_ORANGE,(25,25,25))
            elif mon.border_color != (200,200,200):
                mon.set_border((200,200,200))

        #Draw
        screen.fill(SCREEN_BG)

        for pane in panes:
            pane.update()
            screen.blit(pane.surf,pane.rect)

        sandbox.update(event_list)
        sandbox.draw(screen)
        
        mon_pane.surf.fill(PANE_BG_DARK)
        mon_pane_btn.surf = mon_font.render(stage_sel,False,FG_ORANGE,PANE_BG_LITE)

        for bg in bgs:
            bg_pane.surf.blit(bg.surf,bg.rect)

        preview_pane.surf.blit(bg_sel.surf,(PREVIEW_PANE_W/2 - bg_sel.rect.w/2,PREVIEW_PANE_H/2 - bg_sel.rect.h/2))

        for mon in mons[stage_sel]:
            mon.update()
            mon_pane.surf.blit(mon.surf,(mon.rect.x-mon_pane.rect.left, mon.rect.y-mon_pane.rect.top, 
                                         mon.rect.w, mon.rect.h))

        for i in info:
            i.update()
            screen.blit(i.surf, i.rect)
        if moused_over:
            screen.blit(mon_indicator,(pg.mouse.get_pos()[0]+12, pg.mouse.get_pos()[1]-12))

        menu_bar_file.draw(screen)
        pg.display.flip()

def convert_sprites():
    for r, d, f in os.walk("sprites"):
        for dir in d:
            if not os.path.exists(os.path.join("output",dir)):
                os.mkdir(os.path.join("output",dir))
        for file in f:
            if "png" in file:
            
                filepath = os.path.join(r,file)
                output = os.path.join("output",filepath)
                
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
                spr.save(re.sub('png','bmp',output))
            
def main():
    run_gui()

if __name__ == '__main__':
    main()