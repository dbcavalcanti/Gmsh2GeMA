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
import math
import gemaModel.mesh.auxMeshProcess as aux
from gemaModel.physics.physicsGeMA_Mechanical import physicsGeMA_mechanical
from gemaModel.physics.physicsGeMA_HydroMechanical import physicsGeMA_hydromechanical
from gemaModel.modelGeMA import modelGeMA
from gemaModel.mesh.meshGeMA import gemaMesh
from problemMaterials import problemMaterials

# ===  PROBLEM NAME ===========================================================

problemName = "notchedBeam"

# ===  FOLDER NAME =============================================================

# Define the folder name
folder_name = "gemaFiles"

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

# ===  CREATING THE GEOMETRY ===============================================

# Dimension of the problem: 2D or 3D
dim = 2

# Domain dimensions (m)
Lx  = 0.45
Ly  = 0.10

# Specify the finite element type
#    2 - linear triangles
#    3 - linear quadrilaterals
elementType = 3

# Mesh characteristic lenght
lc = 0.01

# Create the surfaces
surf1 = gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, Lx, 0.02)
surf2 = gmsh.model.occ.addRectangle(0.0, 0.02, 0.0, Lx, Ly-0.02)
surf = [surf1,surf2]

# Discontinuity points
pf1 = gmsh.model.occ.addPoint(Lx/2.0, 0.0, 0.0)
pf2 = gmsh.model.occ.addPoint(Lx/2.0, Ly, 0.0)
d1 = gmsh.model.occ.addLine(pf1, pf2)

# Synchronize the model
gmsh.model.occ.synchronize()

# Set here the surfaces that will compose the mesh domain
beamUnderNotch = gmsh.model.addPhysicalGroup(dim, surf, name='beamUnderNotch')
beamAboveNotch = gmsh.model.addPhysicalGroup(dim, surf, name='beamAboveNotch')
meshDomain     = gmsh.model.addPhysicalGroup(dim, surf, name='ContinuumDomain')

# ===  DEFINITION OF PHYSICAL GROUPS FOR BOUNDARY CONDITIONS =====================

# Get the boundary lines of the domain
bottomBorder = aux.getBoundaryLines(surf, gmsh,np.array([0.0, -1.0, 0.0]))
topBorder    = aux.getBoundaryLines(surf, gmsh,np.array([ 0.0, 1.0, 0.0]))
leftBorder   = aux.getBoundaryLines(surf, gmsh,np.array([-1.0, 0.0, 0.0]))
rightBorder  = aux.getBoundaryLines(surf, gmsh,np.array([ 1.0, 0.0, 0.0]))

# Create the physical groups to apply the boundary conditions on the borders
bottomBorderPG = gmsh.model.addPhysicalGroup( 1, bottomBorder, name='bottomBorder')
topBorderPG    = gmsh.model.addPhysicalGroup( 1, topBorder,    name='topBorder')
leftBorderPG   = gmsh.model.addPhysicalGroup( 1, leftBorder,   name='leftBorder')
rightBorderPG  = gmsh.model.addPhysicalGroup( 1, rightBorder,  name='rightBorder')

# ===  MESH CONFIGURATION =========================================================

# Set the mesh size
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# Combine the triangles to obtain quadrilateral elements
if elementType == 3:  # Quadrilateral element
    gmsh.model.mesh.setRecombine(2, surf1)
    gmsh.model.mesh.setRecombine(2, surf2)

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Generate the mesh
gmsh.option.setNumber("Mesh.Algorithm", 5)
gmsh.model.mesh.generate(2)

# ===  RENUMBER THE NODES  ==============================================

old, new = gmsh.model.mesh.computeRenumbering('RCMK')
gmsh.model.mesh.renumberNodes(old, new)

# ===  MATERIALS AND PHYSICS DEFINITION =================================

# Create a physics that will be used in the simulation
gemaMec  = physicsGeMA_mechanical('PlaneStrain')

# Initialize the model
model = modelGeMA(problemName,[gemaMec])

for material in problemMaterials:
    model.addMaterial(material,problemMaterials[material])

# ===  MESH  =====================================================

# Initialize the mesh object
mesh = gemaMesh(problemName,dim,gmsh)

# Assign domain physical group to the nodes
mesh.setNodesPhysicalGroup(meshDomain)

# Set the materials and physical groups to the mesh
mesh.setCellPhysicalGroup([meshDomain,beamUnderNotch,beamAboveNotch])

# Set the physical groups to the node sets
mesh.setNodeSetData([( 1, topBorderPG),( 1, bottomBorderPG),(1, leftBorderPG),(1, rightBorderPG)])

# Add the mesh to the model
model.setMesh(mesh)

# ===  BOUNDARY CONDITIONS ========================================

model.addBoundaryCondition('node displacements','bcDisplacements',[([0,0],'bottomBorder'),([0,'nil'],'rightBorder'),([0,'nil'],'leftBorder')])

# === WRITE FILES TO GEMA ========================================

# Write the mesh file
mesh.writeMeshFile()
# model.writeModelFile()

# Write the gmsh mesh file
gmsh.write(problemName + ".msh")

# Launch the GUI to see the results:
gmsh.fltk.run()
gmsh.finalize()