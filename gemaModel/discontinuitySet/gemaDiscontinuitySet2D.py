from gemaModel.discontinuitySet.gemaDiscontinuitySet import discontinuitySetGeMA

class discontinuitySetGeMA2D(discontinuitySetGeMA):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triangles = [] 

    def discontinuityData(self):
        pass