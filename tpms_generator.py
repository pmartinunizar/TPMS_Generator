import numpy as np
from scipy.optimize import brentq

##################################################
#           Domain Creation Functions            #
##################################################

##################################################
#        Function: Generate_Grid_Domain          #
##################################################

def Generate_Grid_Domain(Length, Resolution):
    
    """

    Generate a 3D grid within a cubic domain centered at the origin.

    Parameters:
    
        - Length [Float]: The total length of the grid in each dimension.
        - Resolution [Integer]: The number of points along each dimension.

    Returns:

        - XDomain, YDomain, ZDomain [numpy.Ndarray]: Three 3D arrays representing the coordinates X - Y - Z of the grid points in each dimension.

    """    
    
    # Input validation.  
    
    if Resolution is None:
        raise ValueError("Resolution must be provided.")
    if Resolution <= 0:
        raise ValueError("Resolution must be a positive integer")
    if Length is None:
        raise ValueError("Length must be provided.")
    if Length <= 0:
        raise ValueError("Length must be a positive float")
    
    # 3D cube grid domain creation.
    
    Half_Length = np.divide(Length, 2.0)
    Axis = np.linspace(-Half_Length, Half_Length, Resolution)
    XDomain, YDomain, ZDomain = np.meshgrid(Axis, Axis, Axis, indexing='ij')
    
    return XDomain, YDomain, ZDomain
            
##################################################
#          Function: Generate_3D_Domain          #
##################################################

def Generate_3D_Domain(Domain, XDomain, YDomain, ZDomain, Length, Radius, InnerRadius):

    """

    Create a mask domain based on specified geometric shapes. It categories points in the domain as being inside, outside or in the shape's boundary.

    Parameters:
    
        - Domain [String]: The 3D geometric shape selection. 
        - XDomain [numpy.Ndarray]: 3D array representing the X coordinates of the grid points.
        - YDomain [numpy.Ndarray]: 3D array representing the Y coordinates of the grid points.
        - ZDomain [numpy.Ndarray]: 3D array representing the Z coordinates of the grid points.
        - Length [Float]: Edge distance. Parameter used to define X-Y-Z distance for "Cube" and Z for "Cuboid", "Cylinder" and "Ring".
        - Radius [Float]: Radius distance. Parameter used to define X-Y-Z distance for "Sphere" and X-Y for "Cuboid", "Cylinder" and "Ring".
        - InnerRadius [Float]: Inner radius distance. Parameter used to define the inner radius for "Ring" domain.

    Returns:

        - Domain_Mask [numpy.Ndarray]: A 3D array points using boolean category. Where points outside the selected shape are False.
    
    """ 

    # Cube domain creation. 
    
    if Domain == 'Cube':
        Domain_Mask = np.where(
            (np.abs(XDomain) < np.divide(Length, 2.0)) &
            (np.abs(YDomain) < np.divide(Length, 2.0)) &
            (np.abs(ZDomain) < np.divide(Length, 2.0)),
            True,  
            False  
        )

    # Cuboid domain creation.

    elif Domain == 'Cuboid':
        
        if Radius <= 0:
            raise ValueError("Radius must be a positive float")
        
        Domain_Mask = np.where(
            (np.abs(XDomain) < np.divide(Radius, 2.0)) &
            (np.abs(YDomain) < np.divide(Radius, 2.0)) &
            (np.abs(ZDomain) < np.divide(Length, 2.0)),
            True, 
            False  
        )

    # Sphere domain creation.

    elif Domain == 'Sphere':
        
        if Radius <= 0:
            raise ValueError("Radius must be a positive float")
        
        Domain_Mask = np.where(
            np.sqrt(XDomain ** 2 + YDomain ** 2 + ZDomain ** 2) < Radius,
            True,  
            False  
        )   

    # Cylinder domain creation.

    elif Domain == 'Cylinder':
        
        if Radius <= 0:
            raise ValueError("Radius must be a positive float")
        
        Domain_Mask = np.where(
            (np.sqrt(XDomain ** 2 + YDomain ** 2) < Radius) &  
            (np.abs(ZDomain) < np.divide(Length, 2.0)),  
            True,  
            False  
        )

    # Ring domain creation.

    elif Domain == 'Ring':
        
        if Radius <= 0:
            raise ValueError("Radius must be a positive float")
        if InnerRadius is None:
            raise ValueError("Inner radius must be provided for ring domain.")
        if InnerRadius <= 0:
            raise ValueError("Inner radius must be a positive float.")
        if InnerRadius >= Radius:
            raise ValueError("Inner radius must be smaller than the outer radius.")
        
        Domain_Mask = np.where(
            (np.sqrt(XDomain**2 + YDomain**2) > InnerRadius) &             
            (np.sqrt(XDomain**2 + YDomain**2) < Radius) &
            (np.abs(ZDomain) < (np.divide(Length, 2.0))),
            True, False
        )        
        
    return Domain_Mask

##################################################
#          TPMS Equations Implementation         #
##################################################

##################################################
#        Function: Compute_Wave_Functions        #
##################################################
 
def Compute_Wave_Functions(NX, NY, NZ, LX, LY, LZ):
    
    """

    Function to compute the wave numbers (periodic components) to modify the TPMS equations.
    Adjusting the parameters the frequency of the periodic components are modified. 

    Parameters:
    
        - NX [Float]: Number of periodic repetitions along X axis.
        - NY [Float]: Number of periodic repetitions along Y axis.
        - NZ [Float]: Number of periodic repetitions along Z axis.
        - LX [Float]: Length of the unit cell in X dimension.
        - LY [Float]: Length of the unit cell in Y dimension.
        - LZ [Float]: Length of the unit cell in Z dimension.
    
    Returns:
    
        - KX, KY, KZ [Float]: Scalar values representing the wave numbers in X, Y and Z dimensions.
        
    """ 
    
    if NX <= 0:
        raise ValueError("Number of unit cells in X domain must be a positive float")
    if NY <= 0:
        raise ValueError("Number of unit cells in Y domain must be a positive float")
    if NZ <= 0:
        raise ValueError("Number of unit cells in Z domain must be a positive float")
    
    if LX <= 0:
        raise ValueError("Length of unit cells in X domain must be a positive float")
    if LY <= 0:
        raise ValueError("Length of unit cells in Y domain must be a positive float")
    if LZ <= 0:
        raise ValueError("Length of unit cells in Z domain must be a positive float")
    
    # Periodic components calculation.
    
    KX = 2 * np.pi * np.divide(NX, LX)
    KY = 2 * np.pi * np.divide(NY, LY)
    KZ = 2 * np.pi * np.divide(NZ, LZ)
    
    return KX, KY, KZ

##################################################
#          Function: Equation_Selection          #
##################################################

def Equation_Selection(Equation, Topology, XDomain, YDomain, ZDomain, KX, KY, KZ, Isovalue):
    
    """

    Function to select and apply a TPMS equation on the specified 3D topology.

    Parameters:
        
        - Equation [String]: The TPMS equation selection.
        - Topology [String]: Equation condition. 
        - XDomain [numpy.Ndarray]: 3D array representing the X coordinates of the grid points.
        - YDomain [numpy.Ndarray]: 3D array representing the Y coordinates of the grid points.
        - ZDomain [numpy.Ndarray]: 3D array representing the Z coordinates of the grid points.
        - KX [Float]: Scalar value representing the wave value in X dimension.
        - KY [Float]: Scalar value representing the wave value in Y dimension.
        - KZ [Float]: Scalar value representing the wave value in Z dimension.
        - Isovalue [Float]: Constant isovalue.
        
    Returns:

        - TPMS_Equation [numpy.Ndarray]: 3D array containing the TPMS calculated points. 
    
    """ 
    
    TPMS_Equation = np.zeros_like(XDomain)
    
    # Equation selected calculation.
    
    if Equation == 'Primitive':
        TPMS_Equation = np.cos(KX * XDomain) + np.cos(KY * YDomain) + np.cos(KZ * ZDomain)
    elif Equation == 'Gyroid':
        TPMS_Equation = np.sin(KX * XDomain) * np.cos(KY * YDomain) + np.sin(KY * YDomain) * np.cos(KZ * ZDomain) + np.sin(KZ * ZDomain) * np.cos(KX * XDomain)
    elif Equation == 'IWP':
        TPMS_Equation = 2 * ((np.cos(KX * XDomain) * np.cos(KY * YDomain) + np.cos(KY * YDomain) * np.cos(KZ * ZDomain) + np.cos(KZ * ZDomain) * np.cos(KX * XDomain))) - (np.cos(2 * KX * XDomain) + np.cos(2 * KY * YDomain) + np.cos(2 * KZ * ZDomain))
    elif Equation == 'Diamond':
        TPMS_Equation = np.cos(KX * XDomain) * np.cos(KX * YDomain) * np.cos(KZ * ZDomain) - np.sin(KX * XDomain) * np.sin(KY * YDomain) * np.sin(KZ * ZDomain)
    elif Equation == 'Neovius':
        TPMS_Equation = 3 * (np.cos(KX * XDomain) + np.cos(KY * YDomain) + np.cos(KZ * ZDomain)) + 4 * (np.cos(KX * XDomain) * np.cos(KY * YDomain) * np.cos(KZ * ZDomain))
    elif Equation == 'FK-S':
        TPMS_Equation = np.cos(2 * KX * XDomain) * np.sin(KY * YDomain) * np.cos(KZ * ZDomain) + np.cos(KX * XDomain) * np.cos(2 * KY * YDomain) * np.sin(KZ * ZDomain) + np.sin(KX * XDomain) * np.cos(KY * YDomain) * np.cos(2 * KZ *ZDomain)
  
    # Equation topology modification regarding the isovalue.
    
    if Topology == 'Solid 1':
        TPMS_Equation = TPMS_Equation - Isovalue
    elif Topology == 'Solid 2':
        TPMS_Equation = TPMS_Equation + Isovalue    
    elif Topology == 'Sheet':
        TPMS_Equation = (TPMS_Equation - Isovalue) * (TPMS_Equation + Isovalue)
          
    return TPMS_Equation

##################################################
#             Function: Isovalue_Mask            #
##################################################

def Isovalue_Mask(Equation, Domain, Topology, Isovalue, XDomain, YDomain, ZDomain, KX, KY, KZ):

    """

    Simple script to adjust the TPMS equation selected to an specific Isovalue in the desired domain shape.

    Parameters:

        - Equation [String]: The TPMS equation selection.
        - Domain [String]: The 3D geometrical shape selection.
        - Topology [String]: Equation condition. 
        - Isovalue [Float]: Constant isovalue.
        - XDomain [numpy.Ndarray]: 3D array representing the X coordinates of the grid points.
        - YDomain [numpy.Ndarray]: 3D array representing the Y coordinates of the grid points.
        - ZDomain [numpy.Ndarray]: 3D array representing the Z coordinates of the grid points.
        - KX [Float]: Scalar value representing the wave value in X dimension.
        - KY [Float]: Scalar value representing the wave value in Y dimension.
        - KZ [Float]: Scalar value representing the wave value in Z dimension.

    Returns:

        - TPMS [numpy.Ndarray]: 3D array containing the TPMS calculated points inside the limiting 3D domain shape.
    
    """
    
    # Compute the TPMS equation according to the parameters selected.
    
    TPMS = Equation_Selection(Equation, Topology, XDomain, YDomain, ZDomain, KX, KY, KZ, Isovalue)

    # Compute the TPMS selection to the 3D selected domain.
    
    TPMS = - TPMS * Domain
    
    return TPMS

##################################################
#            Function: Density_Value             #
##################################################

def Density_Value(Isovalue, Equation, Domain, Topology, Density, XDomain, YDomain, ZDomain, KX, KY, KZ):
   
    """
    
    Compute the difference between the TPMS density at a given isovalue and the target density.
    
    Parameters:
        
        - Isovalue [Float]: Constant isovalue.
        - Equation [String]: The TPMS equation selection.
        - Domain [String]: The 3D geometrical shape selection.
        - Topology [String]: Equation condition. 
        - Density [Float]: Desired model relative density.
        - XDomain [numpy.Ndarray]: 3D array representing the X coordinates of the grid points.
        - YDomain [numpy.Ndarray]: 3D array representing the Y coordinates of the grid points.
        - ZDomain [numpy.Ndarray]: 3D array representing the Z coordinates of the grid points.
        - KX [Float]: Scalar value representing the wave value in X dimension.
        - KY [Float]: Scalar value representing the wave value in Y dimension.
        - KZ [Float]: Scalar value representing the wave value in Z dimension.
    
    Returns:
    
        - Resulted_Density [Float]: Difference between computed and desired density used for Brent optimisation.
    
    """
    
    # Relative density difference between the TPMS model and the selected domain.
    
    Initial_TPMS = Isovalue_Mask(Equation, Domain, Topology, Isovalue, XDomain, YDomain, ZDomain, KX, KY, KZ)

    Volume_Domain = np.sum(Domain)
    Volume_TPMS = np.sum(Initial_TPMS < 0)

    Current_Density = 1 - np.divide(Volume_TPMS, Volume_Domain)
    Resulted_Density = Current_Density - Density

    return Resulted_Density

##################################################
#          Function: Relative_Density            #
##################################################

def Relative_Density(Equation, Domain, Topology, Density, XDomain, YDomain, ZDomain, KX, KY, KZ):
    
    """
    
    Find optimal isovalue using Brent method and return final TPMS mask.
    
    Parameters:
    
        - Equation [String]: The TPMS equation selection.
        - Domain [String]: The 3D geometrical shape selection.
        - Topology [String]: Equation condition. 
        - Density [Float]: Desired model relative density.
        - XDomain [numpy.Ndarray]: 3D array representing the X coordinates of the grid points.
        - YDomain [numpy.Ndarray]: 3D array representing the Y coordinates of the grid points.
        - ZDomain [numpy.Ndarray]: 3D array representing the Z coordinates of the grid points.
        - KX [Float]: Scalar value representing the wave value in X dimension.
        - KY [Float]: Scalar value representing the wave value in Y dimension.
        - KZ [Float]: Scalar value representing the wave value in Z dimension.

    Returns:
        
        - Final_TPMS [numpy.Ndarray]: 3D binary mask representing the final TPMS structure that matches the requested density.    
    
    """

    # Isovalue bounds depending on topology selection.
    
    if Topology in ["Solid 1", "Solid 2"]:
        Lower_Bound, Upper_Bound = -15.0, 15.0
    elif Topology == "Sheet":
        Lower_Bound, Upper_Bound = 0.0, 15.0

    # Brent method to solve isovalue to required porosity.
    
    Adjusted_Isovalue = brentq(Density_Value, Lower_Bound, Upper_Bound, args=(Equation, Domain, Topology, Density, XDomain, YDomain, ZDomain, KX, KY, KZ))

    # Compute final TPMS mask.
    
    Final_TPMS = Isovalue_Mask(Equation, Domain, Topology, Adjusted_Isovalue, XDomain, YDomain, ZDomain, KX, KY, KZ)

    return Final_TPMS