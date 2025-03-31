import numpy as np
import gmsh

from ogs5py import OGS

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

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
surf1 = gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, Lx, Ly)
surf = [surf1]

# Synchronize the model
gmsh.model.occ.synchronize()

# ===  MESH CONFIGURATION =========================================================

# Set the mesh size
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# Combine the triangles to obtain quadrilateral elements
if elementType == 3:  # Quadrilateral element
    gmsh.model.mesh.setRecombine(2, surf1)

# To see the faces of the elements
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# To see the nodes of the mesh
gmsh.option.setNumber('Mesh.Points', 1)

# Generate the mesh
#gmsh.option.setNumber("Mesh.Algorithm", 5)
mesh = gmsh.model.mesh.generate(2)

model = OGS()
# generate example above
model.msh.import_mesh(mesh, import_dim=2)
model.msh.show()
# generate a predefined grid adapter in 2D
model.msh.generate("grid_adapter2D", in_mat=1, out_mat=0, fill=True)
model.msh.show(show_material_id=True)
# generate a predefined grid adapter in 3D
model.msh.generate("grid_adapter3D", in_mat=1, out_mat=0, fill=True)
model.msh.show(show_material_id=True)
# generate a predefined block adapter in 3D
model.msh.generate("block_adapter3D", xy_dim=5.0, z_dim=1.0, in_res=1)
model.msh.show(show_element_id=True)