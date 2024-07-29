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

problemName = "GulfOfMexico"

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

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

# ===  CREATE THE GEOMETRY =====================================================

gmsh.model.add(problemName)

gmsh.open(os.path.join(problemName_path, "test3horizons1fault.msh"))

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