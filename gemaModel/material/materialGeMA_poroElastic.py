from gemaModel.material.materialGeMA import materialGeMA

class materialGema_poroElastic(materialGeMA):
    def __init__(self, _name, _data):
        super().__init__(_name, _data)
        self.type         = 'poroElastic'
        self.parametersId = ['E','nu','K','gw','Pht','Bp','Kww','Kss','uf','gr','rhob']