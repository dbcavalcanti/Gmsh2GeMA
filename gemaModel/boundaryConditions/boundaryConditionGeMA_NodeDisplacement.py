# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

from gemaModel.boundaryConditions.boundaryConditionGeMA import boundaryConditionsGema

class boundaryConditionsGema_NodeDisplacement(boundaryConditionsGema):
    def __init__(self, _boundaryConditionId,_nodeSetId, _modelDim):
        super().__init__(_boundaryConditionId,'node displacements',_nodeSetId)
        if _modelDim == 2:
            self.parametersId = ['ux','uy']
        elif _modelDim == 3:
            self.parametersId = ['ux','uy','uz']
        self.dim = _modelDim        