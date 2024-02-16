from gemaModel.material.materialGeMA import materialGeMA

class materialGema_elasticInterface(materialGeMA):
    def __init__(self, _name, _data):
        super().__init__(_name, _data)
        self.type         = 'elasticInterface'
        self.parametersId = ['Kn','Ks','Gap','Lkt','Lkb','Iopen']