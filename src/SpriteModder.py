import pygame as pg
import os
from PIL import Image

from config import *

class SpriteModder():

    def __init__(self):
        self.mon_dir = "sprites"
        self.bg_dir = "bg"

        self.palette = []
        self.palette_map = {}

    def update(self, event_list):
        for event in event_list:
            if event.type == CMD_SET_PALETTE:
                self.set_palette(event.path)

    def load_palette(self, path):
        if not path.endswith(".gpl"):
            print("Palette must be in GPL format.")
            return
        if not os.path.exists(path):
            print("File not found.")
            return

        palette = []
        idx = 0
        with open(path, "r") as f:
            for line in f.readlines()[4:]:
                colors = line.split()[:3]
                self.palette_map[idx] = (
                    int(colors[0]),
                    int(colors[1]),
                    int(colors[2]),
                    255
                )
                idx += 1
                for c in colors:
                    palette.append(int(c))
        #Add #FF00FF Transparency Color
        palette.append(255)
        palette.append(0)
        palette.append(255)

        #Real alpha for map
        self.palette_map[idx] = (0,0,0,0)
        
        self.palette = palette
        

    def set_palette(self, path):
        self.load_palette(path)

        p_img = Image.new("P",(16,16))
        p_img.putpalette(self.palette)

        spr = Image.open("out/sprites/child/Agumon.bmp")
        spr_rgb = spr.convert("RGB")
        spr_p = spr_rgb.quantize(colors=65, palette=p_img, dither=0)

        #Manually convert back to alpha png while retaining palette
        spr_w, spr_h = spr_p.size
        spr_out = Image.new("RGBA", (spr_w, spr_h))
        for h in range(0, spr_h):
            for w in range(0, spr_w):
                px = spr_p.getpixel((w, h))
                spr_out.putpixel((w, h), self.palette_map[px])
                
        spr_out.save("agu.png")
        
    def convert_sprites(self, path):
        if path == "":
            path = self.mon_dir
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