from gemaModel.material.materialGeMA import materialGeMA

class materialGema_poroInterfaceMC(materialGeMA):
    def __init__(self, _name, _data):
        super().__init__(_name, _data)
        self.type         = 'poroInterfaceMC'
        self.parametersId = ['Kn','Ks','Cf','Phif','Psif','Tcut','Gap','Lkt','Lkb','Iopen']