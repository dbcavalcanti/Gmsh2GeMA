import numpy as np

# Initialize out of plane vector
ez = np.array([0.0, 0.0, -1.0])

def getBoundaryLines(surface,gmsh,nref):
    """
    Get the boundary lines of a given surface that has the normal vector nref.
    Consider ez = [0.0, 0.0, -1.0]

    Parameters:
    - surface: list of the surfaces to search for the boundary lines
    - gmsh   : Gmsh data structure
    - nref   : reference normal vector (numpy array).
    """
    bndryLines = []
    for surfEntity in surface:
        boundaryEntities = gmsh.model.getBoundary([(2,surfEntity)], False,True)  
        
        for _,boundary in boundaryEntities:
            # Get the nodes associated with the boundary entity
            bndryNodes = gmsh.model.getBoundary([(1,boundary)], False,True) 
            
            # Get the coordinates of the nodes
            Xi = gmsh.model.getValue(0, bndryNodes[0][1],[])
            Xf = gmsh.model.getValue(0, bndryNodes[1][1],[])

            # Compute the tangential vector
            m = np.array(Xf - Xi)

            # Normalize the tangential vector
            m = m / np.linalg.norm(m)

            # Compute the normal vector to the boundary
            n = np.cross(ez,m)

            # If they are in the same direction, add the boundary to the output list
            if np.linalg.norm(n - nref) < 1.0e-15:
                bndryLines.append(abs(boundary))

    return bndryLines