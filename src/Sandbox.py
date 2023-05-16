import pygame as pg
import pickle

from config import *
from Monster import Monster 

class Sandbox(pg.sprite.Sprite):

    def __init__(self):
        super(Sandbox, self).__init__()

        self.surf = pg.Surface((736, SCREEN_H - PAD*2 - 24))
        self.rect = self.surf.get_rect().move(284 + PAD, 24 + PAD)
        self.offset_x = 0
        self.offset_y = 0

        self.tab = 0
        self.mons = []
        self.mons.append(pg.sprite.LayeredUpdates())
        self.mons.append(pg.sprite.LayeredUpdates())

        self.mon_sel = None
        self.preview_mon = None
        self.moused_over_mon = None
        self.font = pg.font.Font('grand9k.ttf',14)

        #Draw grid
        pg.draw.rect(self.surf, (20,20,30), 
                    (0,0,self.rect.w, self.rect.h), border_radius = 4)
        for l in range(0, self.rect.w, 50): #Gridlines
            pg.draw.line(self.surf, (30,30,40), (l,0),
                        (l, self.rect.h), width = 2)
        for l in range(0, self.rect.h, 50):
            pg.draw.line(self.surf, (30,30,40), (0,l),
                        (self.rect.right, l), width = 2)
        pg.draw.rect(self.surf, FG_WHITE, 
                    (0, 0, self.rect.w, self.rect.h), 
                    border_radius=4, width = 2)
        
    def add_mon(self, mon):
        if mon.data.tab == -1:
            mon.data.tab = self.tab
        cur_mon_names = self.get_mon_names(mon.data.tab)
        if mon.data.name not in cur_mon_names:
            self.mons[mon.data.tab].add(mon)

    def remove_mon(self, mon):
        self.mons[self.tab].remove(mon)

    def get_mons(self, tab = -1):
        if tab == -1:
            tab = self.tab
        return self.mons[tab]

    def get_mon_names(self, tab = -1):
        names = []
        if tab == -1:
            for tab in self.mons:
                for mon in tab:
                    names.append(mon.data.name)
        else:
            for mon in self.mons[tab]:
                names.append(mon.data.name)
        return names
    
    def add_tab(self):
        self.mons.append(pg.sprite.LayeredUpdates())

    def change_tab(self, dir):
        self.tab = (self.tab + dir) % len(self.mons)
    
    def save(self):
        out = []
        for tab in self.mons:
            for mon in tab:
                out.append(mon.data)
        with open('save.pkl','wb') as file:
            pickle.dump(out,file)

    def load(self):
        evos = {}
        with open('save.pkl','rb') as file:
            mon_data = pickle.load(file)
            for data in mon_data:
                mon = Monster(data)
                evos[data.name] = mon
                self.add_mon(mon)
        for tab in self.mons:
           for mon in tab:
               for evo_name in mon.data.evos:
                   mon.evos.append(evos[evo_name])

    def export(self):
        out_monster_ref_struct = ""
        out_monster_names = ""
        out_monster_refs = ""

        out_monster_ref_struct = "String filename;"
        out_monster_ref_struct += "\nMonsterName evos[8];"

        for tab in self.mons:
            for mon in tab:
                out_monster_names += mon.data.name + ",\n"

                evos = ""
                for evo in mon.data.evos:
                    evos += evo + ", "
                evos = evos.rstrip(', ')
                if len(evos) == 0:
                    evos = "Agu2006_Digitama"

                out_monster_refs += '{\n\t"' \
                + mon.data.filepath.replace(".png",".bmp") + '",\n' \
                + '\t{' + evos + '}' \
                + '\n},\n'

        out_monster_names = out_monster_names.rstrip(",\n")
        out_monster_refs = out_monster_refs.rstrip(",\n")

        with open("src/template.h") as file:
            f = file.read()
            f = f.replace("out_monster_names", out_monster_names)
            f = f.replace("out_monster_refs", out_monster_refs)
            f = f.replace("out_monster_ref_struct", out_monster_ref_struct)
            with open("out/MonsterDefs.h", "w") as out:
                out.write(f)


    def update(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_d:
                    self.change_tab(1)
                elif event.key == K_a:
                    self.change_tab(-1)
                elif event.key == K_o:
                    self.save()
                elif event.key == K_l:
                    self.load()
                elif event.key == K_e:
                    self.export()
                
            #Drag and Drop
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for mon in self.get_mons():
                        if not mon.rect.collidepoint(event.pos):
                            continue
                        mon.set_border((50,255,0))
                        mon.dragging = True
                        self.mons[self.tab].move_to_front(mon)
                        mouse_x, mouse_y = event.pos
                        self.offset_x = mon.rect.x - mouse_x
                        self.offset_y = mon.rect.y - mouse_y
                        if mon != self.preview_mon:
                            self.preview_mon = mon
                            pg.event.post(
                                pg.event.Event(MON_SELECT,
                                                {"filepath":mon.data.filepath}))
                elif event.button == 2:
                    for mon in self.get_mons():
                        if not mon.rect.collidepoint(event.pos):
                            continue
                        if mon == self.mon_sel:
                            self.mon_sel = None
                        self.remove_mon(mon)
                elif event.button == 3:
                    for mon in self.get_mons():
                        if not mon.rect.collidepoint(event.pos):
                            continue
                        if self.mon_sel == None:
                            self.mon_sel = mon
                            break
                        elif mon in self.mon_sel.evos:
                            self.mon_sel.remove_evo(mon)
                        elif self.mon_sel in mon.evos:
                            mon.remove_evo(self.mon_sel)
                        else:
                            if mon.data.stage != self.mon_sel.data.stage:
                                if (STAGE_ORDER[self.mon_sel.data.stage] 
                                    < STAGE_ORDER[mon.data.stage]):
                                    self.mon_sel.add_evo(mon)
                                else:
                                    mon.add_evo(self.mon_sel)
                        self.mon_sel = None
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    for mon in self.get_mons():
                        mon.dragging = False
                        if not mon.rect.colliderect(self.rect):
                            self.remove_mon(mon)
            elif event.type == pg.MOUSEMOTION:
                for mon in self.get_mons():
                    if mon.dragging:
                        if not mon.rect.colliderect(self.rect):
                            if mon.surf.get_alpha() != 125:
                                mon.surf.set_alpha(125)
                        elif mon.surf.get_alpha() == 125:
                            mon.surf.set_alpha(255)
                        mouse_x, mouse_y = event.pos
                        mon.rect.x = mouse_x + self.offset_x
                        mon.rect.y = mouse_y + self.offset_y
                        mon.data.coords = (mon.rect.x, mon.rect.y)
        
        self.moused_over_mon = None
        for mon in self.get_mons():
            mpos = pg.mouse.get_pos()
            collide = mon.rect.collidepoint(mpos)
            if collide and mon != self.moused_over_mon:
                mon.set_border(FG_WHITE)
                self.moused_over_mon = mon
                self.nameplate = self.font.render(mon.data.name, False,
                                                  FG_ORANGE,(25,25,25))
            elif mon.border_color != ((200,200,200)):
                mon.set_border((200,200,200))
        if self.mon_sel:
            self.mon_sel.set_border((255,135,0))

    def draw(self, surf):
        surf.blit(self.surf, self.rect)

        mons = self.get_mons()
        #Link Lines
        for mon in mons:
            for evo in mon.evos:
                if evo in mons:
                    pg.draw.line(surf, FG_WHITE, 
                                 mon.rect.center, 
                                 evo.rect.center)
        #Monsters
        for mon in mons:
            mon.update()
            surf.blit(mon.surf, mon.rect)

        #Tab Indicator
        tab_indicator = self.font.render(str(self.tab), False, 
                                         (200,200,10), (20,20,30))
        surf.blit(tab_indicator, (self.rect.x+8, self.rect.y+2))

        #Mon Indicator
        mpos = pg.mouse.get_pos()
        if self.moused_over_mon:
            surf.blit(self.nameplate, (mpos[0]+12, mpos[1]-12))
