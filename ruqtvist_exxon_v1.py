# ------------------------------------------------------------------------------
#
# This script reads the OFF files of the geometry, defined by triangulated
# surfaces, and creates a GMSH file with the geometry. 

# Author: Danilo Cavalcanti
# July 2024
#
# ------------------------------------------------------------------------------
import os
import gmsh
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
topSurf    = problemGeometry.loadSurface(os.path.join(problemName_path, "Top_patch_1.off"),"TopSurface")
faultSurf  = problemGeometry.loadSurface(os.path.join(problemName_path, "Fault_patch_1.off"),"FaultSurface")

# List with each type of surface
continuumSurfList = [bottomSurf, topSurf]
faultSurfList     = [faultSurf]

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

# ===  CREATE THE GEOMETRY =====================================================

gmsh.model.add(problemName)

# Create the nodes and the surface in the Gmsh model
problemGeometry.addNodesToGmshModel(gmsh)
problemGeometry.addSurfaceToGmshModel(gmsh)

# === VOLUME GENERATION =========================================================

# Get the tags of top surfaces
topSurfTags = problemGeometry.getGmshSurfaceDimTag(topSurf)

# Get the depth of the model
h = problemGeometry.getModelDepthRange()

# Extension factor
factor = 1.1

# Create the volume by extruding in the "-z" direction the top surface
# volTags = gmsh.model.occ.extrude(topSurfTags, 0, 0, -h*factor)

# === VOLUME FRAGMENTATION =========================================================

# Get the tags of the surfaces associates with the fault surfaces
faultSurfTags = []
for faultSurf in faultSurfList:
    faultSurfTags += problemGeometry.getGmshSurfaceDimTag(faultSurf)

# Get the tags of the surfaces associates with the continuum surfaces
contSurfTags = []
for surf in continuumSurfList:
    contSurfTags += problemGeometry.getGmshSurfaceDimTag(surf)

# Fragment the surfaces and volume with the fault surfaces
# gmsh.model.occ.fragment(faultSurfTags, contSurfTags+volTags)
gmsh.model.occ.fragment(faultSurfTags, contSurfTags)

# Syncronize and update the model
gmsh.model.occ.synchronize()

# ===  MESH GENERATION =========================================================

gmsh.model.mesh.generate(2)
gmsh.write(problemName+".msh")

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Launch the GUI to see the results:
gmsh.fltk.run() 

gmsh.finalize()