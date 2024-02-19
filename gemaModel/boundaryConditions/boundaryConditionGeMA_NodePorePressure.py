# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.boundaryConditions.boundaryConditionGeMA import boundaryConditionsGema

class boundaryConditionsGema_NodePorePressure(boundaryConditionsGema):
    def __init__(self, _boundaryConditionId,_nodeSetId):
        super().__init__(_boundaryConditionId,'node pore pressure',_nodeSetId)
        self.parametersId = ['P']
        self.dim = 1
