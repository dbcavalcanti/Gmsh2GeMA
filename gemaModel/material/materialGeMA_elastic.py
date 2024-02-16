from gemaModel.material.materialGeMA import materialGeMA

class materialGema_elastic(materialGeMA):
    def __init__(self, _name, _data):
        super().__init__(_name, _data)
        self.type         = 'elastic'
        self.parametersId = ['E','nu']