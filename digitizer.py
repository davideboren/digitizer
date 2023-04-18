#
# Converts Transparent .png spritesheets to 24-bit BMPs
# Any transparent pixels are changed to #FF00FF
#

import pygame as pg
from config import *

from PIL import Image
import os
import re

from MonsterImg import MonsterImg

from pygame.locals import (
    K_ESCAPE,
    K_1,K_2,K_3,K_4,K_5,K_6,
    KEYDOWN,
    QUIT
)

def run_gui():

    pg.init()

    pg.display.set_caption("Digitizer")
    pygame_icon = pg.image.load('icon.png')
    pg.display.set_icon(pygame_icon)

    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    clock = pg.time.Clock()

    # Background Panes
    panes = pg.sprite.LayeredUpdates()

    mon_pane = pg.sprite.Sprite()
    mon_pane.surf = pg.Surface((270, SCREEN_HEIGHT - PAD*2 - 24),)
    mon_pane.surf.fill(SCREEN_BG)
    mon_pane.rect = mon_pane.surf.get_rect().move(16,24 + PAD)
    pg.draw.rect(mon_pane.surf, (40,40,40),     (0,0,mon_pane.rect.w, mon_pane.rect.h), border_radius=4)
    pg.draw.rect(mon_pane.surf, (255,255,255),  (0,0,mon_pane.rect.w, mon_pane.rect.h), border_radius=4, width=2)

    sandbox = pg.sprite.Sprite()
    sandbox.surf = pg.Surface((736, SCREEN_HEIGHT - PAD*2 - 24))
    sandbox.rect = sandbox.surf.get_rect().move(mon_pane.rect.right + PAD, 24 + PAD)
    pg.draw.rect(sandbox.surf, (20,20,30),      (0,0,sandbox.rect.w, sandbox.rect.h), border_radius=4)
    for l in range(0,sandbox.rect.w,50): #Gridlines
        pg.draw.line(sandbox.surf,(30,30,40),(l,0),(l,sandbox.rect.h),width=2)
    for l in range(0,sandbox.rect.h,50):
        pg.draw.line(sandbox.surf,(30,30,40),(0,l),(sandbox.rect.right,l),width=2)
    pg.draw.rect(sandbox.surf, (255,255,255),   (0,0,sandbox.rect.w, sandbox.rect.h), border_radius=4, width = 2)

    bg_pane = pg.sprite.Sprite()
    bg_pane.surf = pg.Surface((200,SCREEN_HEIGHT - PAD*3 - 24 - 200))
    bg_pane.rect = bg_pane.surf.get_rect().move(sandbox.rect.right + PAD, 24 + PAD)
    pg.draw.rect(bg_pane.surf, (20,20,30),      (0,0,bg_pane.rect.w, bg_pane.rect.h), border_radius=4)
    pg.draw.rect(bg_pane.surf, (255,255,255),   (0,0,bg_pane.rect.w, bg_pane.rect.h), border_radius=4, width = 2)

    preview_pane = pg.sprite.Sprite()
    preview_pane.surf = pg.Surface((200,200))
    preview_pane.rect = preview_pane.surf.get_rect().move(sandbox.rect.right + PAD, SCREEN_HEIGHT - PAD - 200)
    pg.draw.rect(preview_pane.surf, (20,20,30),      (0,0,preview_pane.rect.w, preview_pane.rect.h), border_radius=4)
    pg.draw.rect(preview_pane.surf, (255,255,255),   (0,0,preview_pane.rect.w, preview_pane.rect.h), border_radius=4, width = 2)

    panes.add(mon_pane)
    panes.add(sandbox)
    panes.add(bg_pane)
    panes.add(preview_pane)
    
    # Monsters
    mons = {}
    x = {}
    y = {}
    cols = 6
    for r,d,f in os.walk("sprites/"):
        for dir in d:
            mons[dir] = pg.sprite.LayeredUpdates()
            x[dir] = 0
            y[dir] = 0
        for file in f:
            if 'png' in file:
                filename = os.path.join(r,file).replace('\\','/')
                fdir = filename.split('/')[1]
                mons[fdir].add(MonsterImg(filename,
                                        (mon_pane.rect[0] + PAD + x[fdir] , 
                                        mon_pane.rect[1] + PAD + y[fdir])))
                x[fdir] = (x[fdir] + 40) % (cols * 40)
                if x[fdir] == 0:
                    y[fdir] += 40

    clicked_mon = MonsterImg
    selected_mons = pg.sprite.LayeredUpdates()

    #Info 
    info = pg.sprite.LayeredUpdates()

    menu_bar = pg.sprite.Sprite()
    menu_bar.surf = pg.Surface((SCREEN_WIDTH, 24))
    menu_bar.rect = menu_bar.surf.get_rect()
    menu_bar.surf.fill((10,30,70))
    pg.draw.line(menu_bar.surf,(5,15,35),
                 (0,menu_bar.rect[3] - 2),
                 (SCREEN_WIDTH,menu_bar.rect[3] - 2),
                 width = 2)

    mon_font = pg.font.Font('grand9k.ttf',14)
    menu_bar_file = pg.sprite.Sprite()
    menu_bar_file.surf = mon_font.render('File',False,(60,90,210),(10,30,70))
    menu_bar_file.rect = menu_bar_file.surf.get_rect().move(2,0)

    info.add(menu_bar)
    info.add(menu_bar_file)

    selected_stage = "baby"

    moused_over = "" 
    mon_indicator = mon_font.render(moused_over,False,(255,220,110),(25,25,25))

    running = True

    while running:
        
        clock.tick(60)
        
        for event in pg.event.get():
        
            #Quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_1:
                    selected_stage = "baby"
                elif event.key == K_2:
                    selected_stage = "baby_ii"
                elif event.key == K_3:
                    selected_stage = "child"
                elif event.key == K_4:
                    selected_stage = "adult"
                elif event.key == K_5:
                    selected_stage = "perfect"
                elif event.key == K_6:
                    selected_stage = "ultimate"
                
            elif event.type == QUIT:
                running = False
                
            #Drag and Drop
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in mons[selected_stage]:
                        if mon.rect.collidepoint(event.pos):
                            selected_mons.add(MonsterImg(mon.filepath,(mon.rect.x,mon.rect.y)))
                    for mon in selected_mons:
                        if mon.rect.collidepoint(event.pos):
                            clicked_mon = mon
                            mon.border_color = (50,255,0)
                            mon.redraw()
                            mon.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = mon.rect.x - mouse_x
                            offset_y = mon.rect.y - mouse_y
                elif event.button == 2:
                    for mon in selected_mons:
                        if mon.rect.collidepoint(event.pos):
                            selected_mons.remove(mon)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    for mon in selected_mons:
                        mon.dragging = False
                        if not mon.rect.colliderect(sandbox.rect):
                            selected_mons.remove(mon)
            elif event.type == pg.MOUSEMOTION:
                for mon in selected_mons:
                    if mon.dragging:
                        if not mon.rect.colliderect(sandbox.rect):
                            if mon.surf.get_alpha() != 125:
                                mon.surf.set_alpha(125)
                        elif mon.surf.get_alpha() == 125:
                            mon.surf.set_alpha(255)
                        mouse_x, mouse_y = event.pos
                        mon.rect.x = mouse_x + offset_x
                        mon.rect.y = mouse_y + offset_y

        moused_over = ""
        for mon in mons[selected_stage]:
            if mon.rect.collidepoint(pg.mouse.get_pos()) and moused_over != mon.name:
                mon.border_color = (255,255,255)
                mon.redraw()
                moused_over = mon.name
                mon_indicator = mon_font.render(mon.name,False,(255,200,100),(25,25,25))
            elif mon.border_color != (200,200,200):
                mon.border_color = (200,200,200)
                mon.redraw()
        for mon in selected_mons:
            if mon.rect.collidepoint(pg.mouse.get_pos()) and moused_over != mon.name:
                mon.border_color = (255,255,255)
                mon.redraw()
                moused_over = mon.name
                mon_indicator = mon_font.render(mon.name,False,(255,200,100),(25,25,25))
            elif mon.border_color != (200,200,200):
                mon.border_color = (200,200,200)
                mon.redraw()

        #Draw
        screen.fill(SCREEN_BG)

        for pane in panes:
            screen.blit(pane.surf,pane.rect)

        for mon in mons[selected_stage]:
            mon.update()
            screen.blit(mon.surf,mon.rect)

        for mon in selected_mons:
            mon.update()
            screen.blit(mon.surf,mon.rect)

        for i in info:
            screen.blit(i.surf, i.rect)
        if moused_over:
            screen.blit(mon_indicator,(pg.mouse.get_pos()[0]+12, pg.mouse.get_pos()[1]-12))

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