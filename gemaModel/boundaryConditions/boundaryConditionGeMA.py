# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.boundaryConditions.boundaryConditionGeMA_variables import bcVariables

class boundaryConditionsGema:

    def __init__(self, _id, _type, _nodeSet):
        self.availableBCtypes       = ['node displacements','node concentrated forces','node pore flow','node pore pressure']
        self.id                     = _id
        self.type                   = _type
        self.nodeSetId              = _nodeSet
        self.parametersId           = []
        self.dim                    = 1

    def setBCid(self, _id):
        self.id = _id

    def setBCtype(self, _type):
        self.type = _type

    def setNodeSetId(self, _nodeSetId):
        self.nodeSetId = _nodeSetId 

    def getBCid(self):
        return self.id  
    
    def getBCtype(self):    
        return self.type

    def writeBoundaryConditionValues(self, _file):
        pass

    def writeBoundaryCondition(self, _file):
        with open (_file,'a') as file:
            file.write('BoundaryCondition {\n')
            file.write('  id = \'' + self.id + '\',\n')
            file.write('  type = \'' + self.type + '\',\n')
            file.write('  mesh = \'mesh\',\n')
            file.write('\n')

            file.write('  properties = {\n')
            for param in self.parametersId:
                file.write(f"    {{id = \'{param}\'")
                file.write(f",  description = \'{bcVariables[param]['description']}\'")
                file.write(f",  unit = \'{bcVariables[param]['unit']}\'")
                file.write(f",  defVal = \'{bcVariables[param]['defVal']}\'")
                file.write(f"}},\n")
            file.write('  },\n')
            file.write('\n')

            file.write('  nodeValues = {\n')
            for value, nodeSet in self.nodeSetId:
                file.write('    {')
                file.write('\'' + nodeSet + '\',')
                for i in range(self.dim):
                    file.write('  ' + str(value[i]) + ',')
                file.write('},\n')
            file.write('  }\n')

            file.write('}\n')
            file.write('\n')

        

