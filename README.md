The main.py file:

*Procedure:
  1) Set the file name in the variable problemName;
  2) Create the geometry and mesh using gmsh;
  3) Create physical groups:
      -   At least one physical group should be created;
      -   A physical group named meshDomain with all surfaces/volumes of the model should be created;
      -   The physical groups will be used to define node sets to apply boundary conditions;
      -   The physical groups will be used to apply the materials to the model;
  4)   Assign the physical groups to the nodes, cell and node sets;
  5)   Define the boundary conditions.

*The name of the physical groups must correspond to the names of the materials in problemMaterials.py

The problemMaterials.py:
  - This file consist in a dictionary with all material parameter values;
  - It must have a final dictionary that gather all materials. The names of the ids in the dictionary, must correspond with the names given to the physical groups.
