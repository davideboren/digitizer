#Class for Monster instances

import pygame
from random import randint

class Monster(pygame.sprite.Sprite):
    def __init__(self, filepath, coords):
    
        super(Monster,self).__init__()
        
        self.filepath = filepath
        self.name = filepath.split('/')[-1].split('.')[0]
        self.stage = filepath.split('/')[-2]
        self.move_style = "walk"
        self.bg = ""
        self.evos = []
        
        self.border_color = (200,200,200)
        self.spritesheet_coords = (0,0)
        self.ticks = randint(0,29)
        
        self.img = pygame.image.load(filepath)
        self.rect = pygame.Rect(0,0,34,34)
        self.surf = pygame.Surface((34,34))
        self.surf.fill(self.border_color)
        self.sprite = pygame.Surface((16,16))
        self.sprite.fill((45,45,45))
        self.sprite.blit(self.img, (0,0), (self.spritesheet_coords,(16,16)))
        self.surf.blit(pygame.transform.scale(self.sprite,(32,32)),(1,1))
        
        self.rect.move_ip(coords)
        self.dragging = False

        
    
    def update(self):
        self.ticks += 1
        if(self.ticks == 30):
            self.spritesheet_coords = (((self.spritesheet_coords[0] + 16) % (32 + randint(0,1)*16),0))
            self.sprite.fill((45,45,45))
            self.sprite.blit(self.img, (0,0), (self.spritesheet_coords,(16,16)))
            self.surf.blit(pygame.transform.scale(self.sprite,(32,32)),(1,1))
            self.ticks = 0

    def redraw(self):
            self.surf.fill(self.border_color)
            self.surf.blit(pygame.transform.scale(self.sprite,(32,32)),(1,1))
