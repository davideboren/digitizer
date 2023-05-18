class MonsterData:
    def __init__(self, **kwargs):
        #Universal
        self.filepath = kwargs.get('filepath', "sprites/adult/Tyrannomon.png")
        default_name = self.filepath.split('/')[-1].split('.')[0]
        self.name = kwargs.get('name', default_name)
        default_stage = self.filepath.split('/')[-2]
        self.stage = kwargs.get('stage', default_stage)
        self.lifespan = kwargs.get('lifespan', 50)
        self.move_style = kwargs.get('move_style', '"walk"')
        default_speed = 0 if self.stage == "digitama" else 2
        self.speed = kwargs.get('speed', default_speed)
        self.bg = kwargs.get('bg', '"bg/bg_0.bmp"')
        self.evos = kwargs.get('evos', [])

        #Digitizer only
        self.tab = kwargs.get('tab', -1)
        self.coords = kwargs.get('coords', (0,0))
