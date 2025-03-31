import gmsh
import math
import sys

import os
import numpy as np
import gmsh
import math
import gemaModel.mesh.auxMeshProcess as aux
from gemaModel.physics.physicsGeMA_Mechanical import physicsGeMA_mechanical
from gemaModel.physics.physicsGeMA_HydroMechanical import physicsGeMA_hydromechanical
from gemaModel.modelGeMA import modelGeMA
from gemaModel.mesh.meshGeMA import gemaMesh
from gemaModel.discontinuitySet.gemaDiscontinuitySet3D import discontinuitySetGeMA3D
from problemMaterials import problemMaterials

# ===  PROBLEM NAME ===========================================================

problemName = "discontinuitySetSurface"

# ===  FOLDER NAME =============================================================

# Define the folder name
folder_name = "gemaFiles"

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

# ===  INITIALIZE GMSH ====================================================

gmsh.initialize(sys.argv)

# create the terrain surface from N x N input data points (here simulated using
# a simple function):
coords = []  # x, y, z coordinates of all the points
nodes = []  # tags of corresponding nodes
tris = []  # connectivities (node tags) of triangle elements
lin = [[], [], [], []]  # connectivities of boundary line elements

# === PARAMETRIC SURFACE =======================================================

def u(_xi,_eta,_zeta):
    return _xi

def v(_xi,_eta,_zeta):
    return _eta

def w(_xi,_eta,_zeta):
    return 0.05*math.sin(10*u(_xi,_eta,_zeta))+0.02*math.sin(10*v(_xi,_eta,_zeta))+0.45*u(_xi,_eta,_zeta)*u(_xi,_eta,_zeta)+0.5

# ===  CREATE GEOMETRY =========================================================

# Define the number of subdivisions of the regular grid
N = 10

# Create a regular grid of N x N points on the unit square [0,1] x [0,1]
def tag(i, j):
    return (N + 1) * i + j + 1

# Create the nodes
count = 0
for i in range(N + 1):
    for j in range(N + 1):
        xn = float(i) / N
        yn = float(j) / N
        gmsh.model.occ.addPoint(u(xn,yn,0),v(xn,yn,0),w(xn,yn,0),tag=count)
        count += 1

# Create regular triangular mesh
tri = []
for j in range(N):
    for i in range(N):
        n1 = i*(N+1)+j
        n2 = (i+1)*(N+1)+j
        tri.append([n1, n2, n2+1])
        tri.append([n2+1, n1+1, n1])

# Create the surfaces
allcurves = {}
for e in tri:
    curves = []
    edgeNodes = e + [e[0]]
    for i in range(len(edgeNodes)-1):
        edge = [edgeNodes[i], edgeNodes[i + 1]]
        ed = tuple(np.sort(edge))
        if ed not in allcurves:
            t = gmsh.model.occ.addLine(edge[0], edge[1])
            allcurves[ed] = t
        else:
            t = allcurves[ed]
        curves.append(t)
    cl = gmsh.model.occ.addCurveLoop(curves)
    s = gmsh.model.occ.addPlaneSurface([cl])

gmsh.model.occ.synchronize()

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.05)

gmsh.model.mesh.generate(2)

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

# ===  CREATE GeMA DISCONTINUITY SET ===============================================

# Create the discontinuity set object
dSet = discontinuitySetGeMA3D(problemName)
dSet.writeDiscontinuitySet()
