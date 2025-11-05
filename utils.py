import numpy as np
from skimage.measure import euler_number
from scipy.ndimage import label
from porespy.filters import local_thickness
from vedo import Mesh

##################################################
#            Mesh Analysis Functions             #
##################################################

##################################################
#             Function: Connectivity             #
##################################################

def Connectivity(TPMS, Domain, Voxel):
    
    """
    
    TPMS solid part topological analysis such as the Betti number.
    
    Parameters:
    
        - TPMS [numpy.Ndarray]: A 3D array containing the TPMS calculated points inside the limiting 3D shape to fit a desired relative density.
        - Domain [String]: The 3D geometrical shape selection.
        - Voxel [Float]: Voxel grid size. 
    
    Returns:
    
        - Nothing.
    
    """
    
    # Select the TPMS solid part.
    
    Solid = ((TPMS >= 0) & Domain.astype(bool)).astype(np.uint8)
    Label, Number = label(Solid, structure=np.ones((3,3,3), int))
    
    if Number > 1:
        Sizes = np.bincount(Label.ravel())
        Sizes[0] = 0  
        Solid = (Label == np.argmax(Sizes)).astype(np.uint8)

    # Calculate the topological analysis parameters.

    Volume = Solid.sum() * (Voxel**3)
    if Volume == 0:
        return dict(b0=0, b1=0, b2=0, chi=0, b1_density=np.nan, volume=0.0)
    
    B0 = 1  
    B2 = Inner_Cavities(Solid.astype(bool))
    Chi = int(euler_number(Solid.astype(np.uint8), connectivity=3))
    B1 = int(B0 + B2 - Chi)
    B1_Density = np.divide(B1, Volume)
    
    print("\n Connectivity statistics for solid TPMS model")
    print(f"  B0 = {B0}  B1 = {B1}  B2 = {B2}  Chi = {Chi}")
    print(f"  B1 density = {B1_Density:.6g}")
    print(f"  Solid volume = {Volume:.6g}")
    
##################################################
#            Function: Inner_Cavities            #
##################################################

def Inner_Cavities(Solid):

    """
    
    Count the internal cavities inside the solid TPMS component within a binary 3D volume.
    
    Parameters:
    
        - Solid [numpy.Ndarray]: 3D binary array representing the TPMS solid region.
        
    Returns:
    
        - Cavities [Integer]: The number of internal cavities inside the solid part.
        
    """
    
    # Define the empty space.
    
    Background = (~Solid).astype(np.uint8)
    
    # Define the connectivity structure.
    
    Structure = np.zeros((3,3,3), dtype=int)
    Structure[1,1,0] = Structure[1,0,1] = Structure[0,1,1] = 1
    Structure[1,1,2] = Structure[1,2,1] = Structure[2,1,1] = 1
    Label, Number = label(Background, structure=Structure)

    if Number == 0:
        return 0
    
    # Identifies the voxels touching the external domain boundary.
    
    Boundary = np.zeros_like(Label, dtype=bool)
    Boundary[0,:,:]=True; Boundary[-1,:,:]=True
    Boundary[:,0,:]=True; Boundary[:,-1,:]=True
    Boundary[:,:,0]=True; Boundary[:,:,-1]=True
    Boundary_Touching = set(np.unique(Label[Boundary]))
    
    # Compute the number of internal cavities.
    
    Cavities = [C for C in np.unique(Label) if (C != 0 and C not in Boundary_Touching)]
    
    return len(Cavities)

##################################################
#           Function: Vertices_Areas             #
##################################################

def Vertices_Surface(Vertices, Faces):
    
    """
    
    Calculate the surface per vertices of the given mesh.
    
    Parameters:
    
        - Vertices [numpy.Ndarray]: Array containing 'n' vertices of the mesh. Each vertex is represented by its 3D coordinates.
        - Faces [numpy.Ndarray]: Array containing 'm' triangular faces of the mesh. Each face is defined by indices that point to the vertices array, specifying the vertices that form each triangle.
        
    Returns:
    
        - Surface [Float]: The surface per vertices.
    
    """
    
    # Obtain the vertices corresponding to each face index.
    
    V0 = Vertices[Faces[:,0]]
    V1 = Vertices[Faces[:,1]]
    V2 = Vertices[Faces[:,2]]
    
    # Compute triangle surfaces.
    
    Face_Surface = 0.5 * np.linalg.norm(np.cross(V1 - V0, V2 - V0), axis=1)
    Number = Vertices.shape[0]
    
    # Distribute each triangle's surface equally among its three vertices.
    
    Surface = np.zeros(Number, dtype=float)
    np.add.at(Surface, Faces[:,0], Face_Surface/3.0)
    np.add.at(Surface, Faces[:,1], Face_Surface/3.0)
    np.add.at(Surface, Faces[:,2], Face_Surface/3.0)
    Surface[Surface<=1e-18] = 1e-18
    
    return Surface

##################################################
#             Function: Curvature                #
##################################################

def Curvature(Vertices, Faces):
   
    """
    
    Calculate the curvature parameters of the TPMS mesh model.

    Parameters:
    
        - Vertices [numpy.Ndarray]: Array containing 'n' vertices of the mesh. Each vertex is represented by its 3D coordinates.
        - Faces [numpy.Ndarray]: Array containing 'm' triangular faces of the mesh. Each face is defined by indices that point to the vertices array, specifying the vertices that form each triangle.

    Returns:
    
        - Nothing.
        
    """
    
    # Build fresh mesh object
    
    Model = Mesh([Vertices, Faces])

    # Compute the mean and the Gaussian curvatures.

    Model.compute_curvature(method=1)
    Mean_Curvature = Model.pointdata["Mean_Curvature"]
    Model.compute_curvature(method=0)
    Gaussian_Curvature = Model.pointdata["Gauss_Curvature"]
    
    # Compute the weighted statistics from the surfaces.
    
    Surface = Vertices_Surface(Vertices, Faces)
    Surface_Weight = Surface / (Surface.sum() + 1e-18)

    # Mean curvature statistics.
    
    H_Absolute = np.abs(Mean_Curvature)
    H_Mean = float((Surface_Weight * H_Absolute).sum())
    K_STD  = float(np.sqrt((Surface_Weight * (H_Absolute - H_Mean)**2).sum()))
    H_P10, H_P50, H_P90 = np.percentile(H_Absolute, [10, 50, 90]).astype(float)

    # Gaussian curvature statistics.
    
    K_Absolute = np.abs(Gaussian_Curvature)
    K_Mean = float((Surface_Weight * K_Absolute).sum())
    K_STD  = float(np.sqrt((Surface_Weight * (K_Absolute - K_Mean)**2).sum()))
    K_P10, K_P50, K_P90 = np.percentile(K_Absolute, [10, 50, 90]).astype(float)

    print("\n Mean curvature analysis for TPMS model:")
    print(f"  Mean: {np.mean(Mean_Curvature):.4f}")
    print(f"  Median: {np.median(Mean_Curvature):.4f}")
    print(f"  Max: {np.max(Gaussian_Curvature):.4f}")
    print(f"  Min: {np.min(Gaussian_Curvature):.4f}")
    
    print("\n Area-Weighted curvature statistics for TPMS model")
    print(f"  |H|: mean = {H_Mean:.4g}, STD = {K_STD:.4g}, " f"P10 = {H_P10:.4g}, P50 = {H_P50:.4g}, P90 = {H_P90:.4g}")
    print(f"  |K|: mean = {K_Mean:.4g}, STD = {K_STD:.4g}, " f"P10 = {K_P10:.4g}, P50 = {K_P50:.4g}, P90 = {K_P90:.4g}")

##################################################
#           Function: Pore_Analysis              #
##################################################

def Pore_Analysis(TPMS, Voxel):
       
    """
    
    Calculates the pore region topological parameters remaining from the TPMS domain.
    
    Parameters:
    
        - TPMS [numpy.Ndarray]: A 3D array containing the TPMS calculated points inside the limiting 3D shape to fit a desired relative density.
        - Voxel [Float]: Voxel grid size. 

    Returns:
    
        - Nothing.
        
    """
    
    # Identify the pore region.
    
    Pore = (TPMS < 0).astype(bool)
    
    # Compute the local thickness of the pore region.
    
    Pore_Thickness = local_thickness(Pore, sizes=range(1, 50))
    Pore_Thickness = Pore_Thickness * Voxel
    Pore_Thickness = Pore_Thickness[Pore & (Pore_Thickness > 0)]
    
    print("\n Pore size statistics using the 3D local thickness algorithm:")
    print(f"  Mean: {np.mean(Pore_Thickness):.3f}")
    print(f"  Median: {np.median(Pore_Thickness):.3f}")
    print(f"  Max: {np.max(Pore_Thickness):.3f}")
    print(f"  Min: {np.min(Pore_Thickness):.3f}")