# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.physics.physicsGeMA import physicsGeMA

class physicsGeMA_mechanical(physicsGeMA):
    def __init__(self, _analysisType):
        super().__init__('Mechanical', _analysisType)
        self.stateVariables = ['u']
        self.name = self.setName(_analysisType)

    def setName(self, _analysisType):
        return self.id + 'FemPhysics.' + _analysisType

    def getPhysicsName(self):
        return self.name
    
    def writeStateVariables(self,problemName):
        fileName = 'gemaFiles\\' + problemName + '_model.lua'
        
