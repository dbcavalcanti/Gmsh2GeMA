class materialGeMA:

    def __init__(self, _name, _data):
        self.availableMaterials     = ['elastic','poroElastic']
        self.name                   = _name
        self.data                   = _data
        self.physics                = 'none'
        self.type                   = 'none'
        self.parametersId           = []
        self.parametersValue        = []
        self.idMaterial             = 0
    
    def setMaterial(self):
        pass

    def fillMaterialParametersValue(self, parametersValue):
        pass

    def setMaterialParameters(self, parameters):
        self.parameters = parameters

    def setMaterialPhysics(self, physics):
        self.physics = physics

    def getMaterialPhysics(self):
        return self.physics

    def getMaterialId(self):
        return self.idMaterial
    
    def getMaterialName(self):
        return self.name
    
    def getMaterialType(self):
        return self.type

    def writePropertySet(self,problemName):
        self.writeHeaderPropertySet(problemName)
        self.writeMaterialProperties(problemName)

    def writeHeaderPropertySet(self,problemName):
        fileName = 'gemaFiles\\' + problemName + '_model.lua'
        with open(fileName, 'a') as file:
            file.write('-------------------------------------------------------------\n')
            file.write('--  Cell properties\n')
            file.write('-------------------------------------------------------------\n')
            file.write('PropertySet\n')
            file.write('{\n')
            file.write('  id= \'MatProp\',\n')
            file.write('  typeName  = \'GemaPropertySet\',\n')
            file.write('  description = \'Material properties\',\n')

    def writeMaterialProperties(self,problemName):
        pass

    def writeMaterialPropertyDescription(self,problemName,parameter):
        fileName = 'gemaFiles\\' + problemName + '_model.lua'
        with open(fileName, 'a') as file:
            file.write('    {id= \'E\',   description = \'Elasticity modulus\',       unit = \'kPa\'},\n')
            file.write('    {id= \'nu\',  description = \'Poisson ratio\',            unit = \'\'},\n')
            file.write('    {id= \'Kss\', description = \'Bulk modulus of grains\',   unit = \'kPa\'},\n')
            file.write('    {id= \'K\',   description = \'Hydraulic permeability\',   unit = \'m/s\'},\n')   
            file.write('    {id= \'Kww\', description = \'Bulk modulus of water\',    unit = \'kPa\'},\n')       
            file.write('    {id= \'gw\',  description = \'Specific weight of water\', unit = \'kN/m3\'},\n')  
            file.write('    {id= \'Pht\', description = \'Porosity\',                 unit = ''},\n')  
            file.write('    {id= \'Bp\',  description = \'Pore compressibility\',     unit = \'1/kPa\'},\n')
