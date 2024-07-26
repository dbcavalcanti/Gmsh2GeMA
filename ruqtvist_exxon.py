# ------------------------------------------------------------------------------
#
# This script reads the OFF files of the geometry, defined by triangulated
# surfaces, and creates a GMSH file with the geometry. 

# Author: Danilo Cavalcanti
# July 2024
#
# ------------------------------------------------------------------------------
import os
import numpy as np
import gmsh
import math
from auxiliar.geometry import geometry

# ===  PROBLEM NAME ===========================================================

problemName = "exxon_1"

# Path to the OFF files of the geometry inside the examples folder
problemName_path = os.path.join(os.getcwd(), "examples", problemName)

# ===  FOLDER NAME =============================================================

# Define the folder name
folder_name = "gemaFiles"

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

# ===  READ THE GEOMETRY =======================================================

# Create the geometry objects for each entity
problemGeometry = geometry()

# Load a surface from an OFF file
bottomSurf = problemGeometry.loadSurface(os.path.join(problemName_path, "Bottom_patch_1.off"),"BottomSurface")
# problemGeometry.loadSurface(os.path.join(problemName_path, "Top_patch_1.off"),"TopSurface")
# problemGeometry.loadSurface(os.path.join(problemName_path, "Fault_patch_1.off"),"FaultSurface")
problemGeometry.getSurfaceCornerPoints(bottomSurf)

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

# gmsh.open(os.path.join(problemName_path, "bottom.msh"))
# gmsh.merge(os.path.join(problemName_path, "top.msh"))

gmsh.model.add(problemName)

# Add the surface
gmsh.model.addDiscreteEntity(2)

# Add all the nodes on the surface (for simplicity... see below):
gmsh.model.mesh.addNodes(2, 1, [], problemGeometry.getCoordinatesVector())

# Add point elements on the 4 points, line elements on the 4 curves, and
# Type 2 for 3-node triangle elements:
gmsh.model.mesh.addElementsByType(1, 2, [], problemGeometry.getTrianglesVector())

# Reclassify the nodes on the curves and the points (since we put them all on
# the surface before with `addNodes' for simplicity)
gmsh.model.mesh.reclassifyNodes()

# Create a geometry for the discrete curves and surfaces, so that we can remesh
# them later on:
gmsh.model.mesh.createGeometry()

gmsh.model.geo.synchronize()

# gmsh.model.mesh.generate(2)
gmsh.write(problemName+".msh")

# # To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# # To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Launch the GUI to see the results:
gmsh.fltk.run() 

gmsh.finalize()