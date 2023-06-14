import pygame as pg
import pickle

from config import *
from Monster import Monster 
from MonsterData import MonsterData
from MonsterDataWidget import MonsterDataWidget

class SandboxPane(pg.sprite.Sprite):

    def __init__(self):
        super(SandboxPane, self).__init__()

        self.surf = pg.Surface((736, SCREEN_H - PAD*2 - 24))
        self.rect = self.surf.get_rect().move(284 + PAD, 24 + PAD)
        self.offset_x = 0
        self.offset_y = 0

        self.tab = 0
        self.mons = []
        self.mons.append(pg.sprite.LayeredUpdates())
        self.mons.append(pg.sprite.LayeredUpdates())
        self.mons.append(pg.sprite.LayeredUpdates())
        self.mons.append(pg.sprite.LayeredUpdates())

        self.mon_sel = None
        self.preview_mon = None
        self.moused_over_mon = None
        self.mon_data_widget = MonsterDataWidget()
        self.mon_data_widget.anchor = (self.rect.right - PAD, 
                                       self.rect.bottom - PAD)

        self.font = pg.font.Font('grand9k.ttf',14)

        self.keys_enabled = True

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
        tab_mon_names = self.get_mon_names(mon.data.tab)
        all_mon_names = self.get_mon_names()
        if mon.data.name not in tab_mon_names:
            instances = 0
            for name in all_mon_names:
                if name == mon.data.name:
                    instances += 1
            self.mons[mon.data.tab].add(mon)
            if instances != 0:
                mon.data.name = mon.data.name + f"_{instances}"

    def remove_mon(self, mon):
        for tab_mon in self.mons[self.tab]:
            if mon.data.name in tab_mon.data.evos:
                tab_mon.data.evos.remove(mon.data.name)
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
    
    def save(self, filename):
        out = []
        for tab in self.mons:
            for mon in tab:
                out.append(mon.data)
        with open(filename,'wb') as file:
            pickle.dump(out,file)

    def load(self, filename):
        self.tab = 0
        self.mons = []
        evos = {}
        with open(filename,'rb') as file:
            mon_data = pickle.load(file)
            for data in mon_data:
                if data.tab > len(self.mons) - 1:
                    self.add_tab()
                mon = Monster(data)
                evos[data.name] = mon
                self.add_mon(mon)
        for tab in self.mons:
           for mon in tab:
               for evo_name in mon.data.evos:
                   mon.evos.append(evos[evo_name])

    def export(self):
        out_monster_names = ""
        out_monster_refs = ""
         
        out_monster_ref_struct = "\
        String filepath;\n\
        MonsterName name;\n\
        MonsterStage stage;\n\
        int lifespan;\n\
        String move_style;\n\
        int speed;\n\
        String bg;\n\
        MonsterName evos[8];"

        rand_egg_data = MonsterData(
            name = "RandomEgg",
            lifespan = 0,
            tab = len(self.mons) - 1,
            coords = (-100,-100)
        )
        rand_egg = Monster(rand_egg_data)
        self.add_mon(rand_egg)

        for tab in self.mons:
            for mon in tab:
                if mon.data.stage == "digitama":
                    rand_egg.data.evos.append(mon.data.name)
                out_monster_names += mon.data.name + ",\n"

                evos = ""
                for evo in mon.data.evos:
                    evos += evo + ", "
                evos = evos.rstrip(', ')
                if len(evos) == 0:
                    evos = "RandomEgg"

                out_monster_refs += '{\n\t"' \
                + mon.data.filepath.replace(".png",".bmp") + '",\n\t' \
                + mon.data.name + ',\n\t' \
                + mon.data.stage + ',\n\t' \
                + str(mon.data.lifespan) + ',\n\t' \
                + mon.data.move_style + ',\n\t' \
                + str(mon.data.speed) + ',\n\t' \
                + mon.data.bg + ',\n\t' \
                + '{' + evos + '}' \
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

        self.remove_mon(rand_egg)
        uc_msg("Exported to out/MonsterDefs.h")


    def update(self, event_list):
        for event in event_list:
            #Drag and Drop
            if event.type == pg.MOUSEBUTTONDOWN:
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
                            self.mon_data_widget.set_mon(mon.data)
                            pg.event.post(
                                pg.event.Event(MON_SELECT,
                                                {"filepath":mon.data.filepath,
                                                 "bg":mon.data.bg}))
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
            elif event.type == BG_SELECT:
                if self.preview_mon:
                    self.preview_mon.data.bg = f'"{event.filepath}"'
            elif event.type == CMD_ACTIVE:
                self.keys_enabled = False
            elif event.type == CMD_INACTIVE:
                self.keys_enabled = True
            elif event.type == CMD_SAVE:
                if event.filename == "":
                    uc_msg("Please enter a filename")
                    break
                elif event.filename.endswith(".pkl"):
                    savefile = event.filename
                else:
                    savefile = event.filename + ".pkl"
                self.save(savefile)
                uc_msg("Saved as " + savefile)
            elif event.type == CMD_LOAD:
                if event.filename.endswith(".pkl"):
                    self.load(event.filename)
                    uc_msg("Loaded " + event.filename)
                else:
                    uc_msg("Invalid filename.")
            elif event.type == CMD_EXPORT:
                self.export()
            elif event.type == CMD_NEW_TAB:
                self.add_tab()
                self.tab = len(self.mons) - 1
                uc_msg(f"Changed to tab {self.tab}")
            elif event.type == KEYDOWN and self.keys_enabled:
                if event.key == K_a:
                    self.change_tab(-1)
                if event.key == K_d:
                    self.change_tab(1)
       
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

        #Widget
        self.mon_data_widget.draw(surf)

        #Mon Indicator
        mpos = pg.mouse.get_pos()
        if self.moused_over_mon:
            surf.blit(self.nameplate, (mpos[0]+12, mpos[1]-12))
