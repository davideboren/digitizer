class MonsterData:
    def __init__(self, **kwargs):
        self.struct = ""

        #Universal
        self.filepath = kwargs.get('filepath', "sprites/adult/Tyrannomon.bmp")
        default_name = self.filepath.split('/')[-1].split('.')[0]
        self.name = kwargs.get('name', default_name)
        default_stage = self.filepath.split('/')[-2]
        self.stage = kwargs.get('stage', default_stage)
        self.move_style = kwargs.get('move_style', "walk")
        self.speed = kwargs.get('speed', 2)
        self.bg = kwargs.get('bg', "")
        self.evos = kwargs.get('evos', [])

        #Digitizer only
        self.tab = kwargs.get('tab', -1)
        self.coords = kwargs.get('coords', (0,0))

        self.struct = "\
        String filepath;\n\
        MonsterName name;\n\
        MonsterStage stage;\n\
        String move_style;\n\
        int speed;\n\
        String bg;\n\
        MonsterName evos[8];\n\
        "