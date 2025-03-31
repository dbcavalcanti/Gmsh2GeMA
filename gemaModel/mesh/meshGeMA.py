# ------------------------------------------------------------------------------
#
# Author: Danilo Cavalcanti
# February 2024
#
# ------------------------------------------------------------------------------

import numpy as np
from gemaModel.mesh.gmsh2GeMA_ElementTypes import gmsh2GeMA_elementTypes
from gemaModel.mesh.gmsh2GeMA_ElementTypes import gmsh2GeMA_elementTypes_NumberOfNodes

class gemaMesh:
    def __init__(self, _problemName, _dim = 2, gmsh = [] , _stateVariables = [],_nodeData = [], _cellData = [], _cellProperties = [], _nodeSetData = []):
        self.gmsh                           = gmsh
        self.id                             = 'mesh'
        self.typeName                       = 'GemaMesh.elem'
        self.description                    = 'Mesh discretization'
        self.coordinateUnits                = 'm'
        self.dim                            = _dim
        self.thickness                      = 1.0
        self.stateVariables                 = _stateVariables
        self.nodeData                       = _nodeData
        self.cellData                       = _cellData
        self.cellProperties                 = _cellProperties
        self.nodeSetData                    = _nodeSetData
        self.hasDiscontinuitySet            = False 
        self.discontinuitySet               = []
        self.nodesPhysicalGroup             = []
        self.cellPhysicalGroups             = []
        self.cellMaterials                  = []
        self.discontinuitySetPhysicalGroup  = []
        self.cellGroups                     = []
        self.elementTypes                   = []
        self.integrationRules               = []
        self.fileName                       = 'gemaFiles\\' + _problemName + '_mesh.lua'

    # ---------------------------------------------------------------------
    def createCellGroup(self):
        pass

    # ---------------------------------------------------------------------
    def setNodesPhysicalGroup(self, _nodesPhysicalGroup):
        self.nodesPhysicalGroup = _nodesPhysicalGroup

    # ---------------------------------------------------------------------
    def setCellPhysicalGroup(self, _cellData):
        self.cellPhysicalGroups = _cellData
            

    # ---------------------------------------------------------------------
    def setNodeSetData(self, _nodeSetData):
        self.nodeSetData = _nodeSetData

    # --------------------------------------------------------------------- 
    def setDiscontinuitySet(self, _discontinuitySet,_discontinuitySetPhysicalGroup):
        self.discontinuitySet              = _discontinuitySet
        self.discontinuitySetPhysicalGroup = _discontinuitySetPhysicalGroup
        self.hasDiscontinuitySet           = True

    # ---------------------------------------------------------------------
    def setDescription(self, _description):
        self.description = _description

    # ---------------------------------------------------------------------
    def setCoordinateUnits(self, _units):
        self.coordinateUnits = _units

    # ---------------------------------------------------------------------
    def setThickness(self, _thickness):
        self.thickness = _thickness
        
    # ---------------------------------------------------------------------    
    def setTypeName(self, _typeName):
        self.typeName = _typeName

    # ---------------------------------------------------------------------   
    def setId(self, _id):
        self.id = _id

    # ---------------------------------------------------------------------   
    def getElementTypes(self):

        elemTypes = []
        for physicalGroupTag in self.cellPhysicalGroups:

            # Get the entities tags associated with this physical group
            entitiesTags = self.gmsh.model.getEntitiesForPhysicalGroup(self.dim,physicalGroupTag)

            # Get the element types present in the physical group with the specified dimension
            for entityTag in entitiesTags:
                entityElemTypes = self.gmsh.model.mesh.getElementTypes(self.dim, entityTag)
                elemTypes.extend(entityElemTypes)
        return list(set(elemTypes))

    # ---------------------------------------------------------------------
    def writeMeshFile(self):
        self.openMeshFile()
        self.printNodes(self.nodesPhysicalGroup)
        self.printElements()
        if self.hasDiscontinuitySet:
            self.printInterfaceElements(self.discontinuitySet,self.discontinuitySetPhysicalGroup)
        self.printNodeSetDataList()
        self.closeMeshFile()

    # ---------------------------------------------------------------------
    # Open the file the mesh file
    def openMeshFile(self):
        
        with open(self.fileName, 'w') as file:
            # Write the header
            file.write("-------------------------------------------------------------\n")
            file.write("-- Mesh definition\n")
            file.write("-------------------------------------------------------------\n")
            
            # Initialize the Lua table with the mesh data
            file.write("\n-- Initialize the mesh data table\n")
            file.write("\nlocal meshData = {}\n")

    # ---------------------------------------------------------------------
    # Close the file the mesh file
    def closeMeshFile(self):
        
        with open(self.fileName, 'a') as file:
            file.write("\nreturn meshData")

    # ---------------------------------------------------------------------
    # Print nodes associated with a physical group   
    def printNodes(self,physicalGroupTag):
        """
        Print the nodes of the mesh that belongs to the given physical group

        Parameters:
        - physicalGroupTag: tag of the physical group which you desire to print the nodes

        """
        
        with open(self.fileName, 'a') as file:
            file.write("\n")
            file.write("-- Nodes coordinates\n")
            file.write("\n")
            file.write("local nodes = {\n")

            _, nodeCoords = self.gmsh.model.mesh.getNodesForPhysicalGroup(self.dim, physicalGroupTag)

            # Reshape the node coordinates into a matrix
            nodeCoords = nodeCoords.reshape((-1,3))

            # Iterate over each row of nodeCoords
            for i, coord in enumerate(nodeCoords, start=1):
                if self.dim == 2:
                    file.write(f"    {{ {coord[0]:.8e}, {coord[1]:.8e} }}, -- {i}\n")
                elif self.dim == 3:
                    file.write(f"    {{ {coord[0]:.8e}, {coord[1]:.8e}, {coord[2]:.8e} }}, -- {i}\n")

            file.write("}\n")

            # Add the nodes to the meshData
            file.write("\nmeshData['nodes'] = nodes\n")

    # ---------------------------------------------------------------------
    # Print elements associated with a physical group with specified element type
    def printElements(self):
        """
        Print the elements of the mesh that belongs to the given physical group
        """

        for physicalGroupTag in self.cellPhysicalGroups:

            # Get the name of the physical group
            physicalGroupName = self.gmsh.model.getPhysicalName(self.dim, physicalGroupTag)

            # Get the entities tags associated with this physical group
            entitiesTags = self.gmsh.model.getEntitiesForPhysicalGroup(self.dim,physicalGroupTag)

            # Get the element types present in the physical group with the specified dimension
            elemTypes = []
            for entityTag in entitiesTags:
                entityElemTypes = self.gmsh.model.mesh.getElementTypes(self.dim, entityTag)
                elemTypes.extend(entityElemTypes)
            elemTypes = list(set(elemTypes))

            # Print the elements of the specified element type 
            with open(self.fileName, 'a') as file:
                for elemType in elemTypes:
                    gemaElement = gmsh2GeMA_elementTypes[elemType]
                    nNodes = gmsh2GeMA_elementTypes_NumberOfNodes[elemType]
                    file.write("\n")
                    file.write(f"-- Mesh {gemaElement} elements of {physicalGroupName}\n")
                    file.write("\n")
                    file.write(f"local {gemaElement}_{physicalGroupName} = {{\n")
                    for e in entitiesTags:
                        _, elem = self.gmsh.model.mesh.getElementsByType(elemType, e)
                        elem = elem.reshape((-1,nNodes))
                        for i, connectivity in enumerate(elem, start=1):
                            file.write("    {")
                            file.write(", ".join(str(node) for node in connectivity))
                            file.write("},\n")
                    file.write("}\n")
                    # Add the elements to the meshData
                    file.write(f"\nmeshData['{gemaElement}_{physicalGroupName}'] = {gemaElement}_{physicalGroupName}\n")


    # ---------------------------------------------------------------------
    # Print nodes associated with a physical group     
    def printNodeSetDataList(self):
        """
        Print the list of nodes of the mesh that belongs to the given physical group

        Parameters:
        - dimPhysicalGroup: dimension of the physical group entities (0 = nodes, 1 = lines, 2 = surfaces)
        - physicalGroupTag: tag of the physical group which you desire to print the nodes
        - gmsh:             Gmsh data structure

        """

        for dimPhysicalGroup,physicalGroupTag in self.nodeSetData:

            # Get the name of the physical group
            physicalGroupName = self.gmsh.model.getPhysicalName(dimPhysicalGroup, physicalGroupTag)

            # Get the entities tags associated with this physical group
            entitiesTags = self.gmsh.model.getEntitiesForPhysicalGroup(dimPhysicalGroup,physicalGroupTag)

            # Get the nodes of the physical group
            nodes = []
            for e in entitiesTags:
                nodeTags = self.gmsh.model.mesh.getNodes(dimPhysicalGroup,e,True)
                for node in nodeTags[0]:
                    nodes.append(node)
            nodes = list(set(nodes))

            # Print the elements of the specified element type 
            with open(self.fileName, 'a') as file:
                file.write("\n")
                file.write(f"-- Node list of {physicalGroupName}\n")
                file.write("\n")
                file.write(f"local nodeList_{physicalGroupName} = {{\n")
                for node in nodes:
                    file.write("    ")
                    file.write(f" {node},\n")
                file.write("}\n")


                # Add the node list to the meshData
                file.write(f"\nmeshData['nodeList_{physicalGroupName}'] = nodeList_{physicalGroupName}\n")


    # ---------------------------------------------------------------------
    # Create 2D zero-thickness double-node interface elements
    def createInterfaceElements(self,discontinuitySet, tripleNode = False):

        # Get the nodes of the continuum domain
        _, nodeCoords,_ = self.gmsh.model.mesh.getNodes()

        # Reshape the node coordinates into a matrix
        nodeCoords = nodeCoords.reshape((-1,3))

        # Get the curves that are associated with the discontinuity
        discontinuityEntitiesTags = self.gmsh.model.getEntitiesForPhysicalGroup(1,discontinuitySet)

        # Get the lines and its nodes associated with the curve
        discontinuity_segmentsID      = []
        discontinuity_segments_curve1 = []
        for i in range((len(discontinuityEntitiesTags)-1)):
            _, discontinuity_segmentsID_i, discontinuity_segments_curve1_i = self.gmsh.model.mesh.getElements(1, discontinuityEntitiesTags[i])
            discontinuity_segmentsID = discontinuity_segmentsID + discontinuity_segmentsID_i
            discontinuity_segments_curve1 = discontinuity_segments_curve1 +  discontinuity_segments_curve1_i

        # Get the lines and its nodes associated with the curve
        _,_, discontinuity_segments_curve2 = self.gmsh.model.mesh.getElements(1, discontinuityEntitiesTags[-1])

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
            nd = np.vstack((np.array(self.gmsh.model.mesh.getNode(discontinuity_nodes1[el][0])[0]), np.array(self.gmsh.model.mesh.getNode(discontinuity_nodes1[el][1])[0])))

            # Find the elements that have each node of the segment
            elem_nd1 = self.gmsh.model.mesh.getElementsByCoordinates(nd[0][0],nd[0][1],nd[0][2],2,True)
            elem_nd2 = self.gmsh.model.mesh.getElementsByCoordinates(nd[1][0],nd[1][1],nd[1][2],2,True)

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
                elementType,edgeNodes,_,_ = self.gmsh.model.mesh.getElement(adj_elements[adjElement])
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
            edgeInterface = [item for sublist in edgeInterface for item in sublist][::-1]
            interfaceElem.append(edgeInterface)

        return interfaceElem

    # ---------------------------------------------------------------------
    # Print the 2D double-node interface elements
            
    def printInterfaceElements(self,interfaceElements,physicalGroupTag):
        """
        Print the zero-thickness interface elements

        Parameters:
        - fileName:          name of the file to print the elements connectivity
        - interfaceElements: list with the connectivity of each interface element
        - physicalGroupTag : tag of the physical group used to create the interface elements
        - gmsh             : Gmsh data structure
        """

        # Get the name of the physical group
        physicalGroupName = self.gmsh.model.getPhysicalName(1, physicalGroupTag)

        # Print the elements of the specified element type 
        #TODO: generalize to other types of interface elements + XFEM
        with open(self.fileName, 'a') as file:
            file.write("\n")
            file.write(f"-- Mesh elements of {physicalGroupName}\n")
            file.write("\n")
            file.write(f"local int2dl4_{physicalGroupName} = {{\n")
            for i, elem in enumerate(interfaceElements, start=1):
                file.write(f"    {{ {elem[0]}, {elem[1]}, {elem[2]}, {elem[3]} }}, -- {i}\n")
            file.write("}\n")

            # Add the node list to the meshData
            file.write(f"\nmeshData['int2dl4_{physicalGroupName}'] = int2dl4_{physicalGroupName}\n")
            

