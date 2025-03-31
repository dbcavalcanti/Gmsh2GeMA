# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# September 2024
#
# ------------------------------------------------------------------------------

class discontinuitySetGeMA:

    def __init__(self, _problemName = 'none'):
        self.name                   = _problemName
        self.description            = 'Discontinuity Set'
        self.additionalPropSet      = []
        self.fileName               = 'gemaFiles\\' + _problemName + '_discontinuitySet.lua'
    
    def discontinuityData(self):
        pass

    def writeDiscontinuitySet(self):
        self.writeHeaderDiscontinuitySet()
        self.writeDiscontinuitySetTable()

    def writeHeaderDiscontinuitySet(self):
        with open(self.fileName, 'a') as file:
            file.write('-------------------------------------------------------------\n')
            file.write('--  Discontinuity Set\n')
            file.write('-------------------------------------------------------------\n')

    def writeDiscontinuitySetTable(self):
        with open(self.fileName, 'a') as file:
            file.write('DiscontinuitySet\n')
            file.write('{\n')
            file.write('  id= \'DSet\',\n')
            file.write('  description = \'Discontinuity set\',\n')
            file.write('  mesh = \'mesh\',\n')
            file.write('  addElements = true\n')
            file.write('}\n')