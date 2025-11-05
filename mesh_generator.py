import numpy as np
from skimage.measure import marching_cubes
from stl import mesh
from vedo import Mesh
import trimesh

##################################################
#              TPMS Model Meshing                #
##################################################

##################################################
#            Function: Generate_Mesh             #
##################################################

def Generate_Mesh(TPMS, Length, Resolution):
    
    """

    Creates a mesh from a 3D scalar field of a TPMS using marching cubes algorithm.
    Function transform the TPMS's scalar field into a geometric representation by identifying on the Iso-surfaces based at a isovalue.
 
    Parameters:

    - TPMS [numpy.Ndarray]: A 3D array containing the TPMS calculated points inside the limiting 3D shape to fit a desired relative density.
    - Length [Float]: Edge distance. Parameter used to define X-Y-Z distance for "Cube" and Z for "Cuboid" and "Cylinder" 
    - Resolution [Integer]: The number of points along each dimension.

    Returns:
    
    - Vertices [numpy.Ndarray]: Array containing 'n' vertices of the mesh. Each vertex is represented by its 3D coordinates.
    - Faces [numpy.Ndarray]: Array containing 'm' triangular faces of the mesh. Each face is defined by indices that point to the vertices array, specifying the vertices that form each triangle.

    """
    
    # Model mesh generation by implementing the marching cubes algorithm.
    
    Spacing = np.divide(Length, Resolution - 1)

    Vertices, Faces, _, _ = marching_cubes(TPMS, level=0, spacing=(Spacing, Spacing, Spacing), method="lewiner")
        
    print(f"Mesh generated with {Vertices.shape[0]} vertices and {Faces.shape[0]} faces.")

    Mesh = trimesh.Trimesh(vertices=Vertices, faces=Faces, process=True)

    # Fix mesh face normals.
    
    Mesh.fix_normals()

    return Vertices, Faces

##################################################
#             Function: Convert_STL              #
##################################################

def Convert_STL(Vertices, Faces, Path):
    
    """
    
    Convert the mesh obtained by marching cubes into a STL file.

    Parameters:
    
        - Vertices [numpy.Ndarray]: Array containing 'n' vertices of the mesh. Each vertex is represented by its 3D coordinates.
        - Faces [numpy.Ndarray]: Array containing 'm' triangular faces of the mesh. Each face is defined by indices that point to the vertices array, specifying the vertices that form each triangle.
        - Path [String]: Directory save location.

    Returns:
    
        - Nothing.        
        
    """

    # Save the mesh model generated in STL format.
    
    Generated_Mesh = mesh.Mesh(np.zeros(Faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(Faces):
        for j in range(3):
            Generated_Mesh.vectors[i][j] = Vertices[f[j], :]

    Generated_Mesh.save(Path)
    Generated_Mesh = trimesh.load_mesh(Path, force='mesh')
    Elements = Generated_Mesh.split(only_watertight=False)
    Elements = [x for x in Elements if x.area >= 0.0]
    
    # Export the obtained STL into the selected path.
    
    if len(Elements) == 0:
        Generated_Mesh.export(Path)
    else:
        Elements.sort(key=lambda y: y.area, reverse=True)
        Generated_Mesh = trimesh.util.concatenate(Elements[:1])
        Generated_Mesh.export(Path)
