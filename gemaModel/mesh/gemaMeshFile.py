import numpy as np

# Open the file the mesh file
def openMeshFile(fileName):
    with open(fileName, 'w') as file:
        # Write the header
        file.write("-------------------------------------------------------------\n")
        file.write("-- Mesh definition\n")
        file.write("-------------------------------------------------------------\n")
        
        # Initialize the Lua table with the mesh data
        file.write("\n-- Initialize the mesh data table\n")
        file.write("\nlocal meshData = {}\n")

# ============================================================================================
# Close the file the mesh file
def closeMeshFile(fileName):
    with open(fileName, 'a') as file:
        file.write("\nreturn meshData")

# ============================================================================================
# Define the correspondency between the element types from  Gmsh with GeMA
def elementNameGmsh2GeMA(elementType):
    if elementType == 2:
        gemaElement = "tri3"
    if elementType == 3:
        gemaElement = "quad4"
    return gemaElement


# ============================================================================================
# Print nodes associated with a physical group
        
def printNodes(fileName,dim,physicalGroupTag,gmsh):
    """
    Print the nodes of the mesh that belongs to the given physical group

    Parameters:
    - fileName:         name of the file to print the nodes coordinates
    - dim:              dimension of the problem (2 = 2D, 3 = 3D)
    - physicalGroupTag: tag of the physical group which you desire to print the nodes
    - gmsh:             Gmsh data structure

    """
    with open(fileName, 'a') as file:
        file.write("\n")
        file.write("-- Nodes coordinates\n")
        file.write("\n")
        file.write("local nodes = {\n")

        _, nodeCoords = gmsh.model.mesh.getNodesForPhysicalGroup(dim, physicalGroupTag)

        # Reshape the node coordinates into a matrix
        nodeCoords = nodeCoords.reshape((-1,3))

        # Iterate over each row of nodeCoords
        for i, coord in enumerate(nodeCoords, start=1):
            if dim == 2:
                file.write(f"    {{ {coord[0]:.8e}, {coord[1]:.8e} }}, -- {i}\n")
            elif dim == 3:
                file.write(f"    {{ {coord[0]:.8e}, {coord[1]:.8e}, {coord[2]:.8e} }}, -- {i}\n")

        file.write("}\n")

        # Add the nodes to the meshData
        file.write("\nmeshData['nodes'] = nodes\n")

# ============================================================================================
# Print elements associated with a physical group with specified element type
        
def printElements(fileName,dim,physicalGroupTag,gmsh):
    """
    Print the elements of the mesh that belongs to the given physical group

    Parameters:
    - fileName:         name of the file to print the elements connectivity
    - dim:              dimension of the problem (2 = 2D, 3 = 3D)
    - physicalGroupTag: tag of the physical group which you desire to print the nodes
    - elementType.      id of the element type of the mesh
    - gmsh:             Gmsh data structure

    """

    # Get the name of the physical group
    physicalGroupName = gmsh.model.getPhysicalName(dim, physicalGroupTag)

    # Get the entities tags associated with this physical group
    entitiesTags = gmsh.model.getEntitiesForPhysicalGroup(dim,physicalGroupTag)

    # Get the element types present in the physical group with the specified dimension
    elemTypes = []
    for entityTag in entitiesTags:
        entityElemTypes = gmsh.model.mesh.getElementTypes(dim, entityTag)
        elemTypes.extend(entityElemTypes)
    elemTypes = list(set(elemTypes))

    # Print the elements of the specified element type 
    with open(fileName, 'a') as file:
        for elemType in elemTypes:
            gemaElement = elementNameGmsh2GeMA(elemType)
            file.write("\n")
            file.write(f"-- Mesh {gemaElement} elements of {physicalGroupName}\n")
            file.write("\n")
            file.write(f"local {gemaElement}_{physicalGroupName} = {{\n")
            for e in entitiesTags:
                _, elem = gmsh.model.mesh.getElementsByType(elemType, e)
                elem = elem.reshape((-1,elemType+1))
                for i, connectivity in enumerate(elem, start=1):
                    file.write("    {")
                    file.write(", ".join(str(node) for node in connectivity))
                    file.write("},\n")
            file.write("}\n")
            # Add the elements to the meshData
            file.write(f"\nmeshData['{gemaElement}_{physicalGroupName}'] = {gemaElement}_{physicalGroupName}\n")

        # with open(fileName, 'a') as file:
        # file.write("\n")
        # file.write(f"-- Mesh elements of {physicalGroupName}\n")
        # file.write("\n")
        # file.write(f"local element_{physicalGroupName} = {{\n")
        # for e in entitiesTags:
        #     _, elem = gmsh.model.mesh.getElementsByType(elementType, e)
        #     elem = elem.reshape((-1,elementType+1))
        #     for i, connectivity in enumerate(elem, start=1):
        #         file.write("    {")
        #         file.write(", ".join(str(node) for node in connectivity))
        #         file.write("},\n")
        # file.write("}\n")

        # # Add the elements to the meshData
        # file.write(f"\nmeshData['element_{physicalGroupName}'] = element_{physicalGroupName}\n")


# ============================================================================================
# Print nodes associated with a physical group
        
def printNodeSetDataList(fileName,dim,physicalGroupTag,gmsh):
    """
    Print the list of nodes of the mesh that belongs to the given physical group

    Parameters:
    - fileName:         name of the file to print the nodes coordinates
    - dim:              dimension of the problem (2 = 2D, 3 = 3D)
    - physicalGroupTag: tag of the physical group which you desire to print the nodes
    - gmsh:             Gmsh data structure

    """

    # Get the name of the physical group
    physicalGroupName = gmsh.model.getPhysicalName(dim, physicalGroupTag)

    # Get the entities tags associated with this physical group
    entitiesTags = gmsh.model.getEntitiesForPhysicalGroup(dim,physicalGroupTag)

    # Print the elements of the specified element type 
    with open(fileName, 'a') as file:
        file.write("\n")
        file.write(f"-- Node list of {physicalGroupName}\n")
        file.write("\n")
        file.write(f"local nodeList_{physicalGroupName} = {{\n")
        for e in entitiesTags:
            nodeTags = gmsh.model.mesh.getNodes(dim,e)
            for node in nodeTags[0]:
                file.write("    ")
                file.write(f" {node},\n")
        file.write("}\n")

        # Add the node list to the meshData
        file.write(f"\nmeshData['nodeList_{physicalGroupName}'] = nodeList_{physicalGroupName}\n")


# ============================================================================================
# Create 2D zero-thickness double-node interface elements
def createInterfaceElements(discontinuitySet,elementType,gmsh):

    # Get the nodes of the continuum domain
    _, nodeCoords,_ = gmsh.model.mesh.getNodes()

    # Reshape the node coordinates into a matrix
    nodeCoords = nodeCoords.reshape((-1,3))

    # Get the mesh continuum elements
    _, elem = gmsh.model.mesh.getElementsByType(elementType, -1)
    elem = elem.reshape((-1,elementType+1))

    # Get the curves that are associated with the discontinuity
    discontinuityEntitiesTags = gmsh.model.getEntitiesForPhysicalGroup(1,discontinuitySet)

    # Get the lines and its nodes associated with the curve
    discontinuity_segmentsID      = []
    discontinuity_segments_curve1 = []
    for i in range((len(discontinuityEntitiesTags)-1)):
        _, discontinuity_segmentsID_i, discontinuity_segments_curve1_i = gmsh.model.mesh.getElements(1, discontinuityEntitiesTags[i])
        discontinuity_segmentsID = discontinuity_segmentsID + discontinuity_segmentsID_i
        discontinuity_segments_curve1 = discontinuity_segments_curve1 +  discontinuity_segments_curve1_i

    # Get the lines and its nodes associated with the curve
    _,_, discontinuity_segments_curve2 = gmsh.model.mesh.getElements(1, discontinuityEntitiesTags[-1])

    discontinuity_segmentsID = [item for sublist in discontinuity_segmentsID for item in sublist]
    discontinuity_segments_curve1 = [item for sublist in discontinuity_segments_curve1 for item in sublist]

    # Convert into a numpy array
    discontinuity_segmentsID = np.array(discontinuity_segmentsID)
    discontinuity_segments_curve1 = np.array(discontinuity_segments_curve1)

    # Reshape the coordinates array 
    discontinuity_nodes1 = discontinuity_segments_curve1.reshape((-1,2))
    discontinuity_nodes2 = discontinuity_segments_curve2[0].reshape((-1,2))

    # Get the number of sub-divisions
    nDiscontinuitySeg = len(discontinuity_segmentsID)

    interfaceElem = []

    for el in range(nDiscontinuitySeg):

        # Get the coordinates of the nodes of the segment
        nd = np.vstack((np.array(gmsh.model.mesh.getNode(discontinuity_nodes1[el][0])[0]), np.array(gmsh.model.mesh.getNode(discontinuity_nodes1[el][1])[0])))

        # Find the elements that have each node of the segment
        elem_nd1 = gmsh.model.mesh.getElementsByCoordinates(nd[0][0],nd[0][1],nd[0][2],2,True)
        elem_nd2 = gmsh.model.mesh.getElementsByCoordinates(nd[1][0],nd[1][1],nd[1][2],2,True)

        # The elements that are adjancent to the line are the ones sharing both nodes
        adj_elements = list(set(elem_nd1) & set(elem_nd2))

        if len(adj_elements) != 2:
            print("Inappropriate number of adjancent elements")
            break

        # Identify the border of the adjacent elements that coincide with the discontinuity
        borderId = []
        edgeInterface = []
        for adjElement in range(2):
            #Get the nodes connectivity of the adjacent element
            _,edgeNodes,_,_ = gmsh.model.mesh.getElement(adj_elements[adjElement])
            edgeNodes = np.concatenate((edgeNodes, [edgeNodes[0]]))
            # Loop through the borders of the element 
            for border in range(elementType+1):
                counter1 = 0
                counter2 = 0
                edge = [edgeNodes[border], edgeNodes[border+1]]
                # Check if the edge has two discontinuity nodes
                if discontinuity_nodes1[el][0] in edge:
                    counter1 += 1
                if discontinuity_nodes1[el][1] in edge:
                    counter1 += 1
                if discontinuity_nodes2[el][0] in edge:
                    counter2 += 1
                if discontinuity_nodes2[el][1] in edge:
                    counter2 += 1
                if (counter1 == 2) or (counter2 == 2):
                    borderId.append(border)
                    edgeInterface.append(edge)
                    break

        # Create the interface element
        edgeInterface = [item for sublist in edgeInterface for item in sublist]
        interfaceElem.append(edgeInterface)

    return interfaceElem

# ============================================================================================
# Print the 2D double-node interface elements
        
def printInterfaceElements(fileName,interfaceElements,physicalGroupTag,gmsh):
    """
    Print the zero-thickness interface elements

    Parameters:
    - fileName:          name of the file to print the elements connectivity
    - interfaceElements: list with the connectivity of each interface element
    - physicalGroupTag : tag of the physical group used to create the interface elements
    - gmsh             : Gmsh data structure
    """

    # Get the name of the physical group
    physicalGroupName = gmsh.model.getPhysicalName(1, physicalGroupTag)

    # Print the elements of the specified element type 
    with open(fileName, 'a') as file:
        file.write("\n")
        file.write(f"-- Mesh elements of {physicalGroupName}\n")
        file.write("\n")
        file.write(f"local int2dl4_element_{physicalGroupName} = {{\n")
        for i, elem in enumerate(interfaceElements, start=1):
            file.write(f"    {{ {elem[0]}, {elem[1]}, {elem[2]}, {elem[3]} }}, -- {i}\n")
        file.write("}\n")

        # Add the node list to the meshData
        file.write(f"\nmeshData['int2dl4_element_{physicalGroupName}'] = int2dl4_element_{physicalGroupName}\n")
        