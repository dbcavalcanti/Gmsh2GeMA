# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# July 2024
#
# ------------------------------------------------------------------------------

import auxiliar.triangulatedSurface as trisurf
import numpy as np

class geometry:

    def __init__(self):
        self.surf  = []     # List of triangulated surfaces objects
        self.triangles   = []     # List of all triangles in the geometry
        self.node = []      # List of all nodes in the geometry

    # ---------------------------------------------------------------------
    def getSurface(self, index):
        return self.surf[index]
    
    # ---------------------------------------------------------------------
    def getTriangle(self, index):     
        return self.triangles[index]  
    
    # ---------------------------------------------------------------------
    def getNode(self, index):
        return self.node[index]
    
    # ---------------------------------------------------------------------
    def getNumSurfaces(self):
        return len(self.surf)   
    
    # --------------------------------------------------------------------- 
    def getNumTriangles(self):
        return len(self.triangles)
    
    # --------------------------------------------------------------------- 
    def getNumNodes(self):
        return len(self.node)
    
    # ---------------------------------------------------------------------
    def getCoordinatesVector(self):
        coordinates = []
        for node in self.node:
            coordinates.extend(node)
        return coordinates
    
    # ---------------------------------------------------------------------
    def getTrianglesVector(self):
        triangles = []
        for triangle in self.triangles:
            triangles.extend(triangle)
        return triangles
    
    # ---------------------------------------------------------------------
    def addNode(self, node):
        self.node.append(node)

    # ---------------------------------------------------------------------
    def addTriangle(self, triangle):
        self.triangles.append(triangle)
    
    # ---------------------------------------------------------------------
    def addSurfaceData(self, surface):

        # Get the current number of nodes
        numNodes = self.getNumNodes()

        # Update the list of triangles
        for i in range(surface.getNumTriangles()):
            triangle = [x + numNodes for x in surface.getTriangle(i)]
            self.addTriangle(triangle)
            surface.globalTriangles.append(triangle)

        # Update the list of surfaces
        self.surf.append(surface)

        # Update the list of coordinates
        for i in range(surface.getNumNodes()):
            self.addNode(surface.getNode(i))

    # ---------------------------------------------------------------------
    def loadSurface(self, file_path, surfaceName):

        # Surface tag
        tag = self.getNumSurfaces()

        # Initialize the triangulated surface object
        surface = trisurf.triangulatedSurface(tag, surfaceName)

        # Read the OFF file
        surface.readOFFFile(file_path)

        # Add the surface to the geometry object
        self.addSurfaceData(surface)

        return tag
    
    # ---------------------------------------------------------------------
    def addNodesToGmshModel(self, gmsh):
        count = 0
        for n in self.node:
            gmsh.model.occ.addPoint(n[0], n[1], n[2],tag=count)
            count += 1

    # ---------------------------------------------------------------------
    def addSurfaceToGmshModel(self, gmsh):
        
        # create a geometrical plane surface for each (triangular) element
        allsurfaces = []
        allcurves = {}

        for surface in self.surf:
            for e in surface.globalTriangles:
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
                surface.gmshTag.append(s)
            allsurfaces.append(surface.gmshTag)

    # ---------------------------------------------------------------------
    def getGmshSurfaceDimTag(self, index):
        return self.surf[index].getGmshDimTag()
    
    # ---------------------------------------------------------------------
    def addVolumeBoundingBox(self,gmsh):
        x = [node[0] for node in self.node]
        y = [node[1] for node in self.node]
        z = [node[2] for node in self.node]
        vol = gmsh.model.occ.addBox(min(x), min(y), min(z), max(x)-min(x), max(y)-min(y), max(z)-min(z))
        return vol
    
    # ---------------------------------------------------------------------
    def getModelDepthRange(self):
        z = [node[2] for node in self.node]
        return abs(max(z)-min(z))
    
    # ---------------------------------------------------------------------
    def getSurfaceCenter(self, surfTag): 
        x = [node[0] for node in self.surf[surfTag].nodes]
        y = [node[1] for node in self.surf[surfTag].nodes]
        z = [node[2] for node in self.surf[surfTag].nodes]
        return [np.mean(x), np.mean(y), np.mean(z)]
    
    # ---------------------------------------------------------------------
    def getVolumeCenter(self): 
        x = [node[0] for node in self.node]
        y = [node[1] for node in self.node]
        z = [node[2] for node in self.node]
        return [np.mean(x), np.mean(y), np.mean(z)]
            