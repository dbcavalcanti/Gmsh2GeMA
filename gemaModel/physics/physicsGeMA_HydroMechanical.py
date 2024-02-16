from gemaModel.physics.physicsGeMA import physicsGeMA

class physicsGeMA_hydromechanical(physicsGeMA):
    def __init__(self, _analysisType):
        super().__init__('CoupledHM', _analysisType)
        self.stateVariables = ['u','p']
        self.name = self.setName(_analysisType)

    def setName(self, _analysisType):
        return self.id + 'FemPhysics.' + _analysisType

    def getPhysicsName(self):
        return self.name
    
    def writeStateVariables(self,problemName):
        fileName = 'gemaFiles\\' + problemName + '_model.lua'
        with open(fileName, 'a') as file:
            file.write("StateVar{id = 'u', dim = 2, description = 'Displacements in the X and Y directions', unit = 'm', format = '8.4f', groupName = 'mechanic'}\n")
            file.write("StateVar{id = 'p', dim = 1, description = 'Pore pressure degree-of-freedom', unit = 'kPa', format = '8.4f', groupName = 'hydraulic'}\n")