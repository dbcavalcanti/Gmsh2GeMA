from gemaModel.physics.physicsGeMA_Mechanical import physicsGeMA_mechanical
from gemaModel.physics.physicsGeMA_HydroMechanical import physicsGeMA_hydromechanical
from gemaModel.modelGeMA import modelGeMA
from problemMaterials import problemMaterials

# Define the problem name
problemName = 'Cappa2011'

# Create a physics that will be used in the simulation
gemaMec  = physicsGeMA_mechanical('PlaneStrain')
gemaHMec = physicsGeMA_hydromechanical('PlaneStrain')

# Initialize the model
m = modelGeMA(problemName,[gemaMec,gemaHMec])

numMaterials = len(problemMaterials)
print('Number of materials: ',numMaterials)

print(problemMaterials['reservoir']['materialType'])

for material in problemMaterials:
    print('Material: ',material)
    m.addMaterial(material,problemMaterials[material])

# Add a material
# m.addMaterial('elastic')
# m.addMaterial('poroElastic',,problemMaterials['reservoir'])

m.writeModelFile()