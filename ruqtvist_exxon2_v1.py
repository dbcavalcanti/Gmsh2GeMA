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
# faultRightSurf = problemGeometry.loadSurface(os.path.join(problemName_path, "Fault_Right_patch_1.off"),"FaultRightSurface")

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
# gmsh.option.setNumber("Geometry.Tolerance", 1e-1)
# gmsh.option.setNumber("Geometry.ToleranceBoolean", 1e-1)
# gmsh.option.setNumber("Mesh.ToleranceReferenceElement", 1e-1)

# ===  CREATE THE GEOMETRY =====================================================

gmsh.model.add(problemName)

# Create the nodes and the surface in the Gmsh model
problemGeometry.addNodesToGmshModel(gmsh)
problemGeometry.addSurfaceToGmshModel(gmsh)

# vol = problemGeometry.addVolumeBoundingBox(gmsh)

# gmsh.model.occ.removeAllDuplicates()

gmsh.model.occ.synchronize()

# === FRAGMENTATION ===========================================================

scalingFactor = 0.05

# Get the tags of the surfaces associates with the continuum surfaces
contSurfTags = problemGeometry.getGmshSurfaceDimTag(bottomSurf)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(bottomAqSurf1)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(bottomAqSurf2)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(bottomAqSurf3)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(topSurf)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(topAqSurf1)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(topAqSurf2)
contSurfTags += problemGeometry.getGmshSurfaceDimTag(topAqSurf3)

Xc = problemGeometry.getVolumeCenter()
gmsh.model.occ.dilate(contSurfTags,Xc[0],Xc[1],Xc[2],1.+scalingFactor,1.+scalingFactor,1.0)
gmsh.model.occ.synchronize()

# Get the tags of the surfaces associates with the fault surfaces
faultSurfTags = problemGeometry.getGmshSurfaceDimTag(faultLeftSurf)
# faultSurfTags += problemGeometry.getGmshSurfaceDimTag(faultRightSurf)


gmsh.model.occ.synchronize()
# Fragment the fault surfaces

gmsh.model.occ.fragment(faultSurfTags, contSurfTags)
# [o1,o2] = gmsh.model.occ.intersect(faultSurfTags, contSurfTags,removeObject=False,removeTool=False)
# gmsh.model.occ.dilate(contSurfTags,Xc[0],Xc[1],Xc[2],1.-scalingFactor,1.-scalingFactor,1.0)
# gmsh.model.occ.fragment(faultSurfTags,[(3,vol)])

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