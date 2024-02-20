import os
import numpy as np
import gmsh
import gemaModel.mesh.auxMeshProcess as aux
from gemaModel.physics.physicsGeMA_Mechanical import physicsGeMA_mechanical
from gemaModel.physics.physicsGeMA_HydroMechanical import physicsGeMA_hydromechanical
from gemaModel.modelGeMA import modelGeMA
from gemaModel.mesh.meshGeMA import gemaMesh
from problemMaterials import problemMaterials
gmsh.initialize()

problemName = "Cappa2011"

# Dimension of the problem: 2D or 3D
dim = 2

# Load mesh and geometry files
gmsh.merge(problemName + ".msh")

# Get all physical groups
physical_groups = gmsh.model.getPhysicalGroups()

def getPhysicalGroupTag(group_name):
    for dim, tag in physical_groups:
        name = gmsh.model.getPhysicalName(dim, tag)
        if name == group_name:
            return tag
    return None

basalAquiferPG   = getPhysicalGroupTag("basalAquifer")
capRockPG        = getPhysicalGroupTag("capRock")
reservoirPG      = getPhysicalGroupTag("reservoir")
upperAquiferPG   = getPhysicalGroupTag("upperAquifer")
bottomBorderPG   = getPhysicalGroupTag("bottomBorder")
leftBorderPG     = getPhysicalGroupTag("leftBorder")
rightBorderPG    = getPhysicalGroupTag("rightBorder")
injPointPG       = getPhysicalGroupTag("injNode")
faultPG          = getPhysicalGroupTag("fault")
meshDomain       = getPhysicalGroupTag("ContinuumDomain")

# ===  MATERIALS AND PHYSICS DEFINITION =================================

# Create a physics that will be used in the simulation
gemaMec  = physicsGeMA_mechanical('PlaneStrain')
gemaHMec = physicsGeMA_hydromechanical('PlaneStrain')

# Initialize the model
model = modelGeMA(problemName,[gemaMec,gemaHMec])

for material in problemMaterials:
    model.addMaterial(material,problemMaterials[material])

# ===  MESH  =====================================================

# Initialize the mesh object
mesh = gemaMesh(problemName,dim,gmsh)

# Create interface elements
interfaceElements = mesh.createInterfaceElements(faultPG)

# Assign domain physical group to the nodes
mesh.setNodesPhysicalGroup(meshDomain)

# Set the materials and physical groups to the mesh
mesh.setCellPhysicalGroup([basalAquiferPG,capRockPG,reservoirPG,upperAquiferPG])

# Set the physical groups to the node sets
mesh.setNodeSetData([( 1, bottomBorderPG),(1, leftBorderPG),(1, rightBorderPG),(0, injPointPG)])

# Set the physical group to the interface elements
mesh.setDiscontinuitySet(interfaceElements,faultPG)

# Add the mesh to the model
model.setMesh(mesh)

# ===  BOUNDARY CONDITIONS ========================================

model.addBoundaryCondition('node displacements','bcDisplacements',[([0,0],'bottomBorder'),([0,'nil'],'rightBorder'),([0,'nil'],'leftBorder')])
model.addBoundaryCondition('node pore flow','bcDischarge',[([-2.0e-5],'injNode')])

# === WRITE FILES TO GEMA ========================================

# Write the mesh file
mesh.writeMeshFile()
model.writeModelFile()


# Launch the GUI to see the results:
gmsh.fltk.run()
gmsh.finalize()