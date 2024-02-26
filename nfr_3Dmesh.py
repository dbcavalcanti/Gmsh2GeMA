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

def generateRandomLinesGmsh(Lx, Ly, n):
    lines_with_tags = []
    for i in range(n):
        x1, y1 = np.random.uniform(0, Lx), np.random.uniform(0, Ly)
        x2, y2 = np.random.uniform(0, Lx), np.random.uniform(0, Ly)
        p1 = gmsh.model.occ.addPoint(x1, y1, 0)
        p2 = gmsh.model.occ.addPoint(x2, y2, 0)
        line = gmsh.model.occ.addLine(p1, p2)
        lines_with_tags.append((1, line))
    return lines_with_tags


# ===  PROBLEM NAME ===========================================================

problemName = "naturallyFracturedReservoir"

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
Lx  = 2000.0
Ly  = 2000.0
Lz  = 1000.0

# Number of fractures
nf = 20

# Generate random lines
lines = generateRandomLinesGmsh(Lx, Ly, nf)

# Create planes
planes = gmsh.model.occ.extrude(lines, 0, 0, Lz)

# Specify the finite element type
#    2 - linear triangles
#    3 - linear quadrilaterals
elementType = 3

# Mesh characteristic lenght
lc = 30.0

# Create the surfaces
volReservoir = gmsh.model.occ.addBox(0.0, 0.0, 0.0, Lx, Ly, Lz)

# Create a division of the surface/volume based on the intersections with
# given lower entities.
o, m = gmsh.model.occ.fragment([(3, volReservoir)], planes)

# Synchronize the model
gmsh.model.occ.synchronize()

# ===  MESH CONFIGURATION =========================================================

# Set the mesh size
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Generate the mesh
gmsh.option.setNumber("Mesh.Algorithm", 1)
gmsh.model.mesh.generate(3)

# ===  RENUMBER THE NODES  ==============================================

old, new = gmsh.model.mesh.computeRenumbering('RCMK')
gmsh.model.mesh.renumberNodes(old, new)

# Launch the GUI to see the results:
gmsh.fltk.run()
gmsh.finalize()