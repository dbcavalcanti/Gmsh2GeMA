# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# July 2024
#
# ------------------------------------------------------------------------------
from scipy.spatial import ConvexHull
import numpy as np

class triangulatedSurface:
    def __init__(self,tag,name):
        self.tag             = tag
        self.name            = name
        self.nodes           = []
        self.triangles       = []
        self.globalTriangles = []
        self.gmshTag         = []

    # --------------------------------------------------------------------- 
    def getSurfaceTag(self):
        return self.tag

    # ---------------------------------------------------------------------
    def getNode(self, index):
        return self.nodes[index]

    # ---------------------------------------------------------------------
    def getTriangle(self, index):
        return self.triangles[index]
    
    # ---------------------------------------------------------------------
    def getNumTriangles(self):
        return len(self.triangles)
    
    # ---------------------------------------------------------------------
    def getNumNodes(self):
        return len(self.nodes)

    # ---------------------------------------------------------------------
    def addNode(self, vertex):
        self.nodes.append(vertex)

    # ---------------------------------------------------------------------
    def addTriangle(self, triangle):
        self.triangles.append(triangle)

    # ---------------------------------------------------------------------
    def getGmshDimTag(self):
        return [(2,tag) for tag in self.gmshTag]

    # ---------------------------------------------------------------------
    # Read the OFF file
    def readOFFFile(self,file_path):
        
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Skip the first line (OFF)
            if lines[0].strip() != 'OFF':
                raise ValueError("Not a valid OFF file")

            # Read the header line containing the number of nodes, faces, and edges
            header = lines[1].strip().split()
            num_nodes = int(header[0])
            num_faces = int(header[1])

            # Read nodes
            for i in range(2, 2 + num_nodes):
                vertex = list(map(float, lines[i].strip().split()))
                self.addNode(vertex)

            # Read faces
            for i in range(2 + num_nodes, 2 + num_nodes + num_faces):
                face_line = list(map(int, lines[i].strip().split()))
                face = face_line[1:]  # Skip the first number which is the number of nodes in the face    
                # self.addTriangle([node + 1 for node in face])
                self.addTriangle(face)
