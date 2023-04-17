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
from AvailMonsPane import AvailMonsPane

from pygame.locals import (
    K_ESCAPE,
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

    availMonsPane = pg.Surface((round(SCREEN_WIDTH/3) - 16, SCREEN_HEIGHT - 16 ))
    
    mons = []
    x = y = 0
    cols = 6
    for r,d,f in os.walk("sprites/baby"):
        for file in f:
            if 'png' in file:
                mons.append(MonsterImg(os.path.join(r,file),(32 + x, 32 + y)))
                
                x = (x + 40) % (cols * 40)
                if x == 0:
                    y += 40
                    
    
    moused_over = "Digimon" 
    mon_font = pg.font.Font('grand9k.ttf',14)
    mon_indicator = mon_font.render(moused_over,False,(255,220,110),(25,25,25))

    #monPane = AvailMonsPane((SCREEN_WIDTH/2,32))
    running = True

    while running:
        
        clock.tick(60)
        
        for event in pg.event.get():
        
            #Quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
                
            #Drag and Drop
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in mons:
                        if mon.rect.collidepoint(event.pos):
                            mon.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = mon.rect.x - mouse_x
                            offset_y = mon.rect.y - mouse_y
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    for mon in mons:
                        mon.dragging = False
            elif event.type == pg.MOUSEMOTION:
                for mon in mons:
                    if mon.dragging:
                        mouse_x, mouse_y = event.pos
                        mon.rect.x = mouse_x + offset_x
                        mon.rect.y = mouse_y + offset_y
        moused_over = ""
        for mon in mons:
            if mon.rect.collidepoint(pg.mouse.get_pos()) and moused_over != mon.name:
                moused_over = mon.name
                mon_indicator = mon_font.render(mon.name.split('\\')[1].split('.')[0],
                                                False,(255,200,100),(25,25,25))

        screen.fill((0,0,32))
        for mon in mons:
            mon.update()
            screen.blit(mon.surf,mon.rect)
        if moused_over:
            screen.blit(mon_indicator,(pg.mouse.get_pos()[0]+12, pg.mouse.get_pos()[1]-12))

        #monPane.update()
        #screen.blit(monPane.surf,(640,16))
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