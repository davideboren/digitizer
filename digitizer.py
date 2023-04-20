#
# Converts Transparent .png spritesheets to 24-bit BMPs
# Any transparent pixels are changed to #FF00FF
#

import pygame as pg
from config import *

from PIL import Image
import os
import re

from Monster import Monster
from Dropdown import Dropdown

def run_gui():

    pg.init()

    pg.display.set_caption("Digitizer")
    pygame_icon = pg.image.load('icon.png')
    pg.display.set_icon(pygame_icon)
    mon_font = pg.font.Font('grand9k.ttf',14)

    screen = pg.display.set_mode((SCREEN_W,SCREEN_H))
    
    clock = pg.time.Clock()

    # Background Panes
    panes = pg.sprite.LayeredUpdates()

    mon_pane_border = pg.sprite.Sprite()
    mon_pane_border.surf = pg.Surface((270, SCREEN_H - PAD*2 - 24),)
    mon_pane_border.surf.fill(SCREEN_BG)
    mon_pane_border.rect = mon_pane_border.surf.get_rect().move(16,24 + PAD)
    pg.draw.rect(mon_pane_border.surf, PANE_BG_COLOR2,     (0,0,mon_pane_border.rect.w, mon_pane_border.rect.h), border_radius=4)
    pg.draw.rect(mon_pane_border.surf, (255,255,255),  (0,0,mon_pane_border.rect.w, mon_pane_border.rect.h), border_radius=4, width=2)
    
    mon_pane = pg.sprite.Sprite()
    mon_pane.surf = pg.Surface((266, SCREEN_H - PAD*2 - 24 - 24 - 2),)
    mon_pane.surf.fill(PANE_BG_COLOR)
    mon_pane.rect = mon_pane.surf.get_rect().move(16 + 2, 24 + 24 + PAD)
    
    mon_pane_btn = pg.sprite.Sprite()
    mon_pane_btn.surf = mon_font.render("Stage",False,(255,220,110),PANE_BG_COLOR2)
    mon_pane_btn.rect = mon_pane_btn.surf.get_rect().move(mon_pane_border.rect.left + 6,mon_pane_border.rect.top + 3)
    
    sandbox = pg.sprite.Sprite()
    sandbox.surf = pg.Surface((736, SCREEN_H - PAD*2 - 24))
    sandbox.rect = sandbox.surf.get_rect().move(mon_pane.rect.right + PAD, 24 + PAD)
    pg.draw.rect(sandbox.surf, (20,20,30), (0,0,sandbox.rect.w, sandbox.rect.h), border_radius=4)
    for l in range(0,sandbox.rect.w,50): #Gridlines
        pg.draw.line(sandbox.surf,(30,30,40),(l,0),(l,sandbox.rect.h),width=2)
    for l in range(0,sandbox.rect.h,50):
        pg.draw.line(sandbox.surf,(30,30,40),(0,l),(sandbox.rect.right,l),width=2)
    pg.draw.rect(sandbox.surf, (255,255,255), (0,0,sandbox.rect.w, sandbox.rect.h), border_radius=4, width = 2)


    bg_pane = pg.sprite.Sprite()
    bg_pane.surf = pg.Surface((BG_PANE_W,BG_PANE_H))
    bg_pane.rect = bg_pane.surf.get_rect().move(sandbox.rect.right + PAD, 24 + PAD)
    pg.draw.rect(bg_pane.surf, PANE_BG_COLOR,      (0,0,bg_pane.rect.w, bg_pane.rect.h), border_radius=4)
    pg.draw.rect(bg_pane.surf, (255,255,255),   (0,0,bg_pane.rect.w, bg_pane.rect.h), border_radius=4, width = 2)

    preview_pane = pg.sprite.Sprite()
    preview_pane.surf = pg.Surface((PREVIEW_PANE_W,PREVIEW_PANE_H))
    preview_pane.rect = preview_pane.surf.get_rect().move(sandbox.rect.right + PAD, SCREEN_H - PAD - 200)
    pg.draw.rect(preview_pane.surf, PANE_BG_COLOR,      (0,0,preview_pane.rect.w, preview_pane.rect.h), border_radius=4)
    pg.draw.rect(preview_pane.surf, (255,255,255),   (0,0,preview_pane.rect.w, preview_pane.rect.h), border_radius=4, width = 2)

    panes.add(mon_pane_border)
    panes.add(mon_pane)
    panes.add(mon_pane_btn)
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
                mons[fdir].add(Monster(filename,
                                        (mon_pane.rect[0] + PAD + x[fdir] , 
                                        mon_pane.rect[1] + PAD + y[fdir])))
                x[fdir] = (x[fdir] + 40) % (cols * 40)
                if x[fdir] == 0:
                    y[fdir] += 40

    selected_mons = pg.sprite.LayeredUpdates()

    bgs = pg.sprite.LayeredUpdates()
    bg_sel = None

    for r,d,f in os.walk("bg/"):
        for file in f:
            if 'png' in file:
                filepath = os.path.join(r,file).replace('\\','/')
                bg = pg.sprite.Sprite()
                bg.img = pg.image.load(filepath)
                bg.surf = pg.Surface((128+2,128+2))
                bg.surf.fill((255,255,255))
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

    menu_bar_file = Dropdown("File")

    info.add(menu_bar)
    info.add(menu_bar_file)

    stage_sel = list(STAGE_ORDER.keys())[0]

    moused_over = "" 
    mon_indicator = mon_font.render(moused_over,False,(255,220,110),(25,25,25))

    mon_sel = None

    running = True

    while running:
        
        clock.tick(60)
        
        for event in pg.event.get():

            menu_bar_file.handleEvents(event)
        
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key in STAGE_KEYS.keys():
                    stage_sel = STAGE_KEYS[event.key]
            elif event.type == QUIT:
                running = False
                
            #Drag and Drop
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    selected_mon_names = [mon.name for mon in selected_mons]
                    for mon in mons[stage_sel]:
                        if mon.rect.collidepoint(event.pos) and mon.name not in selected_mon_names:
                            selected_mons.add(Monster(mon.filepath,(mon.rect.x,mon.rect.y)))
                    for mon in selected_mons:
                        if mon.rect.collidepoint(event.pos):
                            mon.set_border((50,255,0))
                            mon.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = mon.rect.x - mouse_x
                            offset_y = mon.rect.y - mouse_y
                elif event.button == 2:
                    for mon in selected_mons:
                        if mon.rect.collidepoint(event.pos):
                            if mon == mon_sel:
                                mon_sel = None
                            selected_mons.remove(mon)
                elif event.button == 3:
                    for mon in selected_mons:
                        if mon.rect.collidepoint(event.pos):
                            if mon_sel == None:
                                mon_sel = mon
                                break
                            elif mon in mon_sel.evos:
                                mon_sel.evos.remove(mon)
                            elif mon_sel in mon.evos:
                                mon.evos.remove(mon_sel)
                            else:
                                if mon.stage != mon_sel.stage:
                                    if STAGE_ORDER[mon_sel.stage] < STAGE_ORDER[mon.stage]:
                                        mon_sel.evos.append(mon)
                                    else:
                                        mon.evos.append(mon_sel)
                            mon_sel = None
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
            elif event.type == pg.MOUSEWHEEL:
                mouse_pos = pg.mouse.get_pos()
                if mon_pane.rect.collidepoint(mouse_pos):
                    mon_pane.surf.scroll(0,event.y*15)
                    for mon in mons[stage_sel]:
                        mon.rect.y += 15*event.y

        mouse_pos = pg.mouse.get_pos()
        moused_over = ""
        for mon in mons[stage_sel]:
            if mon.rect.collidepoint(mouse_pos) and mon.rect.colliderect(mon_pane.rect) and moused_over != mon.name:
                mon.set_border((255,255,255))
                moused_over = mon.name
                mon_indicator = mon_font.render(mon.name,False,(255,200,100),(25,25,25))
            elif mon.border_color != (200,200,200):
                mon.set_border((200,200,200))
        for mon in selected_mons:
            if mon.rect.collidepoint(mouse_pos) and moused_over != mon.name:
                mon.set_border((255,255,255))
                moused_over = mon.name
                mon_indicator = mon_font.render(mon.name,False,(255,200,100),(25,25,25))
            elif mon.border_color != (200,200,200):
                mon.set_border((200,200,200))
        if mon_sel:
            mon_sel.set_border((255,135,0))

        #Draw
        screen.fill(SCREEN_BG)

        for pane in panes:
            pane.update()
            screen.blit(pane.surf,pane.rect)
        
        mon_pane.surf.fill(PANE_BG_COLOR)
        mon_pane_btn.surf = mon_font.render(stage_sel,False,(250,170,0),PANE_BG_COLOR2)

        for bg in bgs:
            bg_pane.surf.blit(bg.surf,bg.rect)

        preview_pane.surf.blit(bg_sel.surf,(PREVIEW_PANE_W/2 - bg_sel.rect.w/2,PREVIEW_PANE_H/2 - bg_sel.rect.h/2))

        for mon in mons[stage_sel]:
            mon.update()
            mon_pane.surf.blit(mon.surf,(mon.rect.x-mon_pane.rect.left, mon.rect.y-mon_pane.rect.top, 
                                         mon.rect.w, mon.rect.h))

        for mon in selected_mons:
            for evo in mon.evos:
                if evo in selected_mons:
                    pg.draw.line(screen,(255,255,255),mon.rect.center,evo.rect.center)
        for mon in selected_mons:
            mon.update()
            screen.blit(mon.surf,mon.rect)

        for i in info:
            i.update()
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