# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

class physicsGeMA:
    def __init__(self, _id = 'none', _analysisType = 'none'):
        self.availablePhysics       = ['Mechanical','Hydro','CoupledHM','CoupledTM']
        self.availableAnalysisTypes = ['PlaneStrain','PlaneStress','Axisymmetric','3D','Flow']
        self.name                   = 'none' 
        self.id                     = _id
        self.analysisType           = _analysisType 
        self.stateVariables         = 'none'

    def getPhysicsName(self):
        pass

    def writeStateVariables(self):
        pass
    
    def getPhysicsStateVariables(self):
        return self.stateVariables
    