# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.boundaryConditions.boundaryConditionGeMA import boundaryConditionsGema

class boundaryConditionsGema_NodePoreFlow(boundaryConditionsGema):
    def __init__(self, _boundaryConditionId,_nodeSetId):
        super().__init__(_boundaryConditionId,'node pore flow',_nodeSetId)
        self.parametersId = ['qw']
        self.dim = 1