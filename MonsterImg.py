import pygame
from random import randint

class MonsterImg(pygame.sprite.Sprite):
    def __init__(self, filepath, coords):
    
        super(MonsterImg,self).__init__()
        
        self.name = filepath.split('/')[-1].split('.')[0]
        
        self.border_color = (200,200,200)
        self.spritesheet_coords = (0,0)
        self.ticks = randint(0,29)
        
        self.spr = pygame.image.load(filepath)
        self.rect = pygame.Rect(0,0,34,34)
        self.surf = pygame.Surface((34,34))
        self.surf.fill((255,255,255))
        
        sprite = pygame.Surface((16,16))
        sprite.fill((45,45,45))
        sprite.blit(self.spr, (0,0), (self.spritesheet_coords,(16,16)))
        self.surf.blit(pygame.transform.scale(sprite,(32,32)),(1,1))
        #pygame.draw.rect(self.surf,self.border_color,(0,0,34,34))
        
        self.rect.move_ip(coords)
        self.dragging = False
    
    def update(self):
        self.ticks += 1
        if(self.ticks == 30):
            self.spritesheet_coords = (((self.spritesheet_coords[0] + 16) % (32 + randint(0,1)*16),0))
            sprite = pygame.Surface((16,16))
            sprite.fill((45,45,45))
            sprite.blit(self.spr, (0,0), (self.spritesheet_coords,(16,16)))
            self.surf.blit(pygame.transform.scale(sprite,(32,32)),(1,1))
            self.ticks = 0

