# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.boundaryConditions.boundaryConditionGeMA import boundaryConditionsGema

class boundaryConditionsGema_NodeConcentratedForce(boundaryConditionsGema):
    def __init__(self, _boundaryConditionId,_nodeSetId, _modelDim):
        super().__init__(_boundaryConditionId,'node concentrated forces',_nodeSetId)
        self.parametersId = ['f']
        self.dim = _modelDim