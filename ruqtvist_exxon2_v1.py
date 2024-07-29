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

problemName = "exxon_2"

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
bottomSurf     = problemGeometry.loadSurface(os.path.join(problemName_path, "Bottom_patch_1.off"),"BottomSurface1")
bottomAqSurf1  = problemGeometry.loadSurface(os.path.join(problemName_path, "Bottom_Aquifer_patch_1.off"),"BottomAqSurface1")
bottomAqSurf2  = problemGeometry.loadSurface(os.path.join(problemName_path, "Bottom_Aquifer_patch_2.off"),"BottomAqSurface2")
bottomAqSurf3  = problemGeometry.loadSurface(os.path.join(problemName_path, "Bottom_Aquifer_patch_3.off"),"BottomAqSurface3")
topSurf        = problemGeometry.loadSurface(os.path.join(problemName_path, "Top_patch_1.off"),"TopSurface")
topAqSurf1     = problemGeometry.loadSurface(os.path.join(problemName_path, "Top_Aquifer_patch_1.off"),"TopAqSurface1")
topAqSurf2     = problemGeometry.loadSurface(os.path.join(problemName_path, "Top_Aquifer_patch_2.off"),"TopAqSurface1")
topAqSurf3     = problemGeometry.loadSurface(os.path.join(problemName_path, "Top_Aquifer_patch_3.off"),"TopAqSurface2")
faultLeftSurf  = problemGeometry.loadSurface(os.path.join(problemName_path, "Fault_Left_patch_1.off"),"FaultLeftSurface")
faultRightSurf = problemGeometry.loadSurface(os.path.join(problemName_path, "Fault_Right_patch_1.off"),"FaultRightSurface")

# List with each type of surface
# continuumSurfList = [bottomSurf, bottomAqSurf1, bottomAqSurf2, bottomAqSurf3, topSurf, topAqSurf1, topAqSurf2, topAqSurf3]
continuumSurfList = [bottomSurf,topSurf,bottomAqSurf2,topAqSurf2,topAqSurf3,topAqSurf1]
faultSurfList     = [faultLeftSurf,faultRightSurf]

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.option.setNumber("Geometry.Tolerance", 1e-1)
gmsh.option.setNumber("Geometry.ToleranceBoolean", 1)
gmsh.option.setNumber("Mesh.ToleranceReferenceElement", 1e-1)
# gmsh.option.setNumber("Geometry.SnapX", 1)
# gmsh.option.setNumber("Geometry.SnapY", 1)
# gmsh.option.setNumber("Geometry.SnapZ", 1)


# ===  CREATE THE GEOMETRY =====================================================

gmsh.model.add(problemName)

# Create the nodes and the surface in the Gmsh model
problemGeometry.addNodesToGmshModel(gmsh)
problemGeometry.addSurfaceToGmshModel(gmsh)

gmsh.model.occ.synchronize()

# === VOLUME GENERATION =========================================================

# Get the tags of top surfaces
topSurfTags = problemGeometry.getGmshSurfaceDimTag(topSurf)

# Get the depth of the model
h = problemGeometry.getModelDepthRange()

# Extension factor
factor = 1.5

# Create the volume by extruding in the "-z" direction the top surface
volTags = gmsh.model.occ.extrude(topSurfTags, 0, 0, -h*factor)

gmsh.model.occ.synchronize()

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
# gmsh.model.occ.fragment(contSurfTags, faultSurfTags)
gmsh.model.occ.fragment(volTags, faultSurfTags)

# Syncronize and update the model
gmsh.model.occ.synchronize()

# ===  MESH GENERATION =========================================================

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 50.0)

# gmsh.model.mesh.generate(3)
gmsh.write(problemName+".msh")

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Launch the GUI to see the results:
gmsh.fltk.run() 

gmsh.finalize()