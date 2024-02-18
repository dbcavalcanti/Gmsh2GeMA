# ------------------------------------------------------------------------------
#
# This script generate the mesh of the fault reactivation problem presented by
# Cappa and Rutqvist (2011). The mesh is conform to the fault, the nodes along 
# the fault are duplicated and double-node interface elements are created.
#
# Author: Danilo Cavalcanti
# February 2024
#
# Reference:
#   Cappa, F., & Rutqvist, J. (2011). Modeling of coupled deformation and
#   permeability evolution during fault reactivation induced by deep 
#   underground injection of CO2. International Journal of Greenhouse Gas
#   Control, 5(2), 336-346. https://doi.org/10.1016/j.ijggc.2010.08.005
#
# ------------------------------------------------------------------------------
import os
import numpy as np
import gmsh
import gemaModel.mesh.auxMeshProcess as aux
from gemaModel.physics.physicsGeMA_Mechanical import physicsGeMA_mechanical
from gemaModel.physics.physicsGeMA_HydroMechanical import physicsGeMA_hydromechanical
from gemaModel.modelGeMA import modelGeMA
from gemaModel.mesh.meshGeMA import gemaMesh
from problemMaterials import problemMaterials

# ===  FOLDER NAME =============================================================

# Define the folder name
folder_name = "gemaFiles"

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

# ===  PROBLEM NAME ===========================================================

problemName = "Cappa2011"

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

# ===  CREATING THE GEOMETRY ===============================================

# Dimension of the problem: 2D or 3D
dim = 2

# Domain dimensions (m)
Lx  = 2000.0
Ly  = 2000.0

# Specify the finite element type
#    2 - linear triangles
#    3 - linear quadrilaterals
elementType = 3

# Mesh characteristic lenght
lc = 100.0

# Create the surfaces
surfBasalAquifer = gmsh.model.occ.addRectangle(0.0,    0.0, 0.0, 2000.0, 800.0)
surfLowerCapRock = gmsh.model.occ.addRectangle(0.0,  800.0, 0.0, 2000.0, 150.0)
surfReservoir    = gmsh.model.occ.addRectangle(0.0,  950.0, 0.0, 2000.0, 100.0)
surfUpperCapRock = gmsh.model.occ.addRectangle(0.0, 1050.0, 0.0, 2000.0, 150.0)
surfUpperAquifer = gmsh.model.occ.addRectangle(0.0, 1200.0, 0.0, 2000.0, 800.0)

# Fault points
pf1 = gmsh.model.occ.addPoint(323.6730193,    0.0, 0.0)
pf2 = gmsh.model.occ.addPoint(676.3269807, 2000.0, 0.0)

# Fault
fault = gmsh.model.occ.addLine(pf1, pf2)

# Injection point
injPoint = gmsh.model.occ.addPoint(0.0, 1000.0, 0.0)

# Create a division of the surface/volume based on the intersections with
# given lower entities.
o, m = gmsh.model.occ.fragment([(2, surfBasalAquifer),(2, surfLowerCapRock),(2, surfReservoir),(2, surfUpperCapRock),(2, surfUpperAquifer)], [(1, fault),(0,injPoint)])

# Synchronize the model
gmsh.model.occ.synchronize()

# ===  DEFINITION OF THE PHYSICAL GROUPS FOR MATERIALS  ==================================

# Get the children entities. The order that they are listed in "m" is the same that
# they were passed as inputs in the fragmentation function.
children_surfBasalAquifer  = m[0]
children_surfLowerCapRock  = m[1]
children_surfReservoir     = m[2]
children_surfUpperCapRock  = m[3]
children_surfUpperAquifer  = m[4]
children_fault             = m[5]

# Get the children surfaces
#    children_surf[:][0] is the dimension of the entity. In this case is 2 since is a surface
#    children_surf[:][1] is the tag of the child entity. 
new_surfBasalAquifer = [surf_i[1] for surf_i in children_surfBasalAquifer]
new_surfLowerCapRock = [surf_i[1] for surf_i in children_surfLowerCapRock]
new_surfReservoir    = [surf_i[1] for surf_i in children_surfReservoir]
new_surfUpperCapRock = [surf_i[1] for surf_i in children_surfUpperCapRock]
new_surfUpperAquifer = [surf_i[1] for surf_i in children_surfUpperAquifer]

# Get the children lines
new_fault = [line_i[1] for line_i in children_fault]

# Create a list with all the surfaces
all_surfaces = new_surfBasalAquifer + new_surfLowerCapRock + new_surfReservoir + new_surfUpperCapRock + new_surfUpperAquifer

# Set here the surfaces that will compose the mesh domain
meshDomain = gmsh.model.addPhysicalGroup(dim, all_surfaces, name='ContinuumDomain')

# Define additional physical groups to set the materials
basalAquiferPG = gmsh.model.addPhysicalGroup(dim,   new_surfBasalAquifer, name='BasalAquifer')
lowerCapRockPG = gmsh.model.addPhysicalGroup(dim,   new_surfLowerCapRock, name='LowerCapRock')
reservoirPG    = gmsh.model.addPhysicalGroup(dim,   new_surfReservoir,    name='Reservoir')
upperCapRockPG = gmsh.model.addPhysicalGroup(dim,   new_surfUpperCapRock, name='UpperCapRock')
upperAquiferPG = gmsh.model.addPhysicalGroup(dim,   new_surfUpperAquifer, name='UpperAquifer')
faultPG        = gmsh.model.addPhysicalGroup(dim-1, new_fault,            name='Fault')

# ===  DEFINITION OF PHYSICAL GROUPS FOR BOUNDARY CONDITIONS =====================

# Get the boundary lines of the domain
bottomBorder = aux.getBoundaryLines(new_surfBasalAquifer,gmsh,np.array([0.0, -1.0, 0.0]))
topBorder    = aux.getBoundaryLines(new_surfUpperAquifer,gmsh,np.array([ 0.0, 1.0, 0.0]))
leftBorder   = aux.getBoundaryLines(all_surfaces,        gmsh,np.array([-1.0, 0.0, 0.0]))
rightBorder  = aux.getBoundaryLines(all_surfaces,        gmsh,np.array([ 1.0, 0.0, 0.0]))

# Create the physical groups to apply the boundary conditions on the borders
bottomBorderPG = gmsh.model.addPhysicalGroup( 1, bottomBorder, name='bottomBorder')
topBorderPG    = gmsh.model.addPhysicalGroup( 1, topBorder,    name='topBorder')
leftBorderPG   = gmsh.model.addPhysicalGroup( 1, leftBorder,   name='leftBorder')
rightBorderPG  = gmsh.model.addPhysicalGroup( 1, rightBorder,  name='rightBorder')

# Create the physical groups to apply the boundary conditions on a specific node
injPointPG = gmsh.model.addPhysicalGroup( 0, [injPoint], name='injNode')

# ===  MESH CONFIGURATION =========================================================

# Set the mesh size
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# Combine the triangles to obtain quadrilateral elements
for surf_i in all_surfaces:
    if elementType == 3:  # Quadrilateral element
        gmsh.model.mesh.setRecombine(2, surf_i)

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Generate the mesh
gmsh.option.setNumber("Mesh.Algorithm", 1)
gmsh.model.mesh.generate(2)

# ===  DUPLICATE NODES ALONG THE FAULT ===================================

gmsh.plugin.setNumber("Crack", "Dimension", 1)
gmsh.plugin.setNumber("Crack", "PhysicalGroup", faultPG)
gmsh.plugin.run("Crack")

# ===  RENUMBER THE NODES  ==============================================

old, new = gmsh.model.mesh.computeRenumbering('RCMK')
gmsh.model.mesh.renumberNodes(old, new)

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

# Assign the physical groups to mesh entities
mesh.setNodesPhysicalGroup(meshDomain)
mesh.setCellPhysicalGroup([basalAquiferPG,lowerCapRockPG,reservoirPG,upperCapRockPG,upperAquiferPG])
mesh.setNodeSetData([(1, bottomBorderPG),(1, leftBorderPG),(1, rightBorderPG),(0, injPointPG)])
mesh.setDiscontinuitySet(interfaceElements,faultPG)

# === WRITE FILES TO GEMA ========================================

# Write the mesh file
mesh.writeMeshFile()
model.writeModelFile()

# Launch the GUI to see the results:
gmsh.fltk.run()
gmsh.finalize()