class materialGeMA:

    def __init__(self, name, includeSectionPropSet = True):
        self.availableMaterials = ['elastic','saturated']
        self.name = name
        self.physics = 'none'
        self.type = 'none'
        self.parameters = []
        self.idMaterial = 0
        self.addSecPropSet = includeSectionPropSet
        self.idSection = 0

    def setMaterial(self):
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
        if self.addSecPropSet == True:
            self.writeSectionProperties(problemName)

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

    def writeSectionProperties(self,problemName):
        fileName = 'gemaFiles\\' + problemName + '_model.lua'
        with open(fileName, 'a') as file:
            file.write('PropertySet\n')
            file.write('{\n')
            file.write('  id= \'SectionProp\',\n')
            file.write('  typeName  = \'GemaPropertySet\',\n')
            file.write('  description = \'Section properties\',\n')
            file.write('  properties  = {\n')  
            file.write('     {id = \'h\',	description = \'Element thickness\',	unit = \'m\'},\n')
            file.write('  },\n') 
            file.write('  values  = {\n')   
            file.write('    {h = 1.0},\n')  
            file.write('  }\n')   
            file.write('}\n\n') 

    def writeMaterialProperties(self):
        pass
