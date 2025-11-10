"""


        :::   :::    ::::::::  :::::::::  ::::::::::               ::::::::  :::::::::   ::::::::  :::    ::: ::::::::: 
      :+:+: :+:+:  :+:    :+: :+:    :+: :+:                     :+:    :+: :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
    +:+ +:+:+ +:+       +:+  +:+    +:+ +:+                     +:+        +:+    +:+ +:+    +:+ +:+    +:+ +:+    +:+  
   +#+  +:+  +#+     +#+    +#++:++#+  +#++:++#  +#++:++#++:++ :#:        +#++:++#:  +#+    +:+ +#+    +:+ +#++:++#+    
  +#+       +#+   +#+      +#+    +#+ +#+                     +#+   +#+# +#+    +#+ +#+    +#+ +#+    +#+ +#+           
 #+#       #+#  #+#       #+#    #+# #+#                     #+#    #+# #+#    #+# #+#    #+# #+#    #+# #+#            
###       ### ########## #########  ##########               ########  ###    ###  ########   ########  ###     


Author: Pablo Martín Compaired 
Contact: pablo.martin@unizar.es
Department: M2BE
University: Zaragoza University [UNIZAR]
Version: 1.0
Date: Sep 17, 2025

Description:

    Custom application to generate simple 3D geometry models with a TPMS pattern. Modelled by the Isovalue or the desired relative density.

Usage:
    
    1. Select the geometry parameters using the combo-box and the keyboard.
    2. Press "Display" button to generate the desired geometry. After calculating the geometry will be displayed at the UI.
    3. Press "Export STL" button to export the desired geometry in STL format.

License:

    This project is licensed under the MIT License. See the LICENSE file for details.

Future updates:

    - Incorporate the gradient TPMS implementation at simple domains.
    - Export the model at different formats.

"""

################################################################################################
# Main libraries import:
import sys
import os
import vtk
# Custom functions import:
from tpms_generator import *
from mesh_generator import *
from utils import Connectivity, Curvature, Pore_Analysis
################################################################################################
# UI modules import:
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QCoreApplication
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkPolyDataMapper, vtkActor
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor, vtkCubeAxesActor
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkCommonDataModel import vtkPolyData, VTK_TRIANGLE
################################################################################################
# UI APP directory:
script_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(script_dir, 'UI')
sys.path.append(ui_dir)
from UIoutput import Ui_MainWindow
################################################################################################

# Main window UI function definitions.

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('TPMS: Simple Geometries')
        
        # Import lab logo.

        LOGO = os.path.join(ui_dir, 'logo_m2be_2024.png')
        self.labelLogo.setPixmap(QPixmap(LOGO))
        self.labelLogo.setScaledContents(True)  
        self.Visibility(self.labelRadius, False)
        self.Visibility(self.labelRadius_Inner, False)
        self.Visibility(self.lineEditRadius, False)
        self.Visibility(self.lineEditRadius_Inner, False)
        
        # Set default parameters to line edit sections.
        
        self.lineEditX.setText("1")
        self.lineEditY.setText("1")
        self.lineEditZ.setText("1")
        
        self.lineEditLX.setText("1")
        self.lineEditLY.setText("1")
        self.lineEditLZ.setText("1")
        
        self.lineEditHeight.setText("1")
        
        self.lineEditResolution.setText("50")
        self.lineEditDensity.setText("0.3")
        
        # Populate combo box panels:
        
        self.Populate_ComboBox(self.comboBoxEquation, ["Gyroid", "Diamond", "Primitive", "IWP", "Neovius", "FK-S"])
        self.Populate_ComboBox(self.comboBoxDomain, ["Cube", "Cuboid", "Sphere", "Cylinder", "Ring"] )
        self.Populate_ComboBox(self.comboBoxTopology, ["Solid 1", "Solid 2", "Sheet"])
        self.Populate_ComboBox(self.comboBoxMethod, ["Relative Density", "Constant Isovalue"])
        self.comboBoxMethod.currentIndexChanged.connect(self.Update_Method_Text)
        self.comboBoxDomain.currentIndexChanged.connect(self.Update_Domain_Text)
        
        # Initialize visuals setup:
        
        self.meshData = None
        self.Initialise_VTK_Components()
        self.Default_Model()
        print("Initialization complete.")
        
        # Button actions:
        
        self.pushButtonDisplay.clicked.connect(self.Compute)
        self.pushButtonExport.clicked.connect(self.Export)

    def Update_Method_Text(self):  
        
        # Updating text in method option.

        Method_Text = self.comboBoxMethod.currentText()

        if Method_Text == "Relative Density":
            self.labelResolution_2.setText(QCoreApplication.translate("MainWindow", "Select Relative Density:", None))
            
        elif Method_Text == "Constant Isovalue":
            self.labelResolution_2.setText(QCoreApplication.translate("MainWindow", "Select Constant Isovalue:", None))
            
    def Visibility(self, widget, visible):
        
        # Custom function to hide or show components.
        
        if visible:
            widget.setMaximumHeight(16777215)  
            widget.setMinimumHeight(0)  
        else:
            widget.setMaximumHeight(0)  
            widget.setMinimumHeight(0)  

    def Update_Domain_Text(self):
        
        # Enabling and displaying the different line edits according to the domain selection.

        Domain_Text = self.comboBoxDomain.currentText()
        
        if Domain_Text == "Cube":
            self.Visibility(self.labelHeight, True)
            self.Visibility(self.lineEditHeight, True)
            self.labelHeight.setText(QCoreApplication.translate("MainWindow", "Length:", None))
            self.Visibility(self.labelRadius, False)
            self.Visibility(self.labelRadius_Inner, False)
            self.Visibility(self.lineEditRadius, False)
            self.Visibility(self.lineEditRadius_Inner, False)
            self.lineEditRadius.clear()
            self.lineEditHeight.clear()
            self.lineEditRadius_Inner.clear()
    
        elif Domain_Text == "Cuboid":
            self.Visibility(self.labelHeight, True)
            self.Visibility(self.lineEditHeight, True)
            self.labelHeight.setText(QCoreApplication.translate("MainWindow", "Height:", None))
            self.Visibility(self.labelRadius, True)
            self.Visibility(self.labelRadius_Inner, False)
            self.Visibility(self.lineEditRadius, True)
            self.Visibility(self.lineEditRadius_Inner, False)
            self.labelRadius.setText(QCoreApplication.translate("MainWindow", "Width:", None))
            self.lineEditHeight.clear()
            self.lineEditRadius.clear()
            self.lineEditRadius_Inner.clear()

        elif Domain_Text == "Cylinder":
            self.Visibility(self.labelHeight, True)
            self.Visibility(self.lineEditHeight, True)
            self.labelHeight.setText(QCoreApplication.translate("MainWindow", "Height:", None))
            self.Visibility(self.labelRadius, True)
            self.Visibility(self.lineEditRadius, True)
            self.Visibility(self.labelRadius_Inner, False)
            self.Visibility(self.lineEditRadius_Inner, False)
            self.labelRadius.setText(QCoreApplication.translate("MainWindow", "Radius:", None))
            self.lineEditHeight.clear()
            self.lineEditRadius.clear()
            self.lineEditRadius_Inner.clear()

        elif Domain_Text == "Sphere":
            self.Visibility(self.labelHeight, False)
            self.Visibility(self.lineEditHeight, False)
            self.Visibility(self.labelRadius, True)
            self.Visibility(self.lineEditRadius, True)
            self.Visibility(self.labelRadius_Inner, False)
            self.Visibility(self.lineEditRadius_Inner, False)
            self.labelRadius.setText(QCoreApplication.translate("MainWindow", "Radius:", None))
            self.lineEditHeight.clear()
            self.lineEditRadius.clear()
            self.lineEditRadius_Inner.clear()
            
        elif Domain_Text == "Ring":
            self.Visibility(self.labelHeight, True)
            self.Visibility(self.lineEditHeight, True)
            self.Visibility(self.labelRadius, True)
            self.Visibility(self.lineEditRadius, True)
            self.Visibility(self.labelRadius_Inner, True)
            self.Visibility(self.lineEditRadius_Inner, True)
            self.labelHeight.setText(QCoreApplication.translate("MainWindow", "Height:", None))
            self.labelRadius.setText(QCoreApplication.translate("MainWindow", "Exterior Radius:", None))
            self.labelRadius_Inner.setText(QCoreApplication.translate("MainWindow", "Inner Radius:", None))
            self.lineEditHeight.clear()
            self.lineEditRadius.clear()
            self.lineEditRadius_Inner.clear()
            
    def Populate_ComboBox(self, comboBox, items):
        
        # Adding combo-box components: 

        comboBox.addItems(items)  

    def Show_Error(self, message):
        
        # Window emerging show error message:   

        QMessageBox.critical(self, "Error", message)

    def Mesh_Info(self, PolyData):
        
        # Mesh display info: nodes and elements. 
        
        Nodes = PolyData.GetNumberOfPoints()
        Elements = PolyData.GetNumberOfCells()

        print(f"Number of Nodes: {Nodes}")
        print(f"Number of Elements: {Elements}")

    def Predefined_Camera(self):
        
        # Set a predefined camera angle for the model displayed.
        
        Camera = self.Renderer.GetActiveCamera()
        isometric_position = [1, 1, 1]
        Camera.SetPosition(isometric_position)
        Camera.SetFocalPoint(0, 0, 0)
        Camera.SetViewUp(0, 0, 1)
        self.Renderer.ResetCamera()
        Camera.ParallelProjectionOn()

    def Display_Mesh(self, vertices, faces):
        
        # Display and render the TPMS model generated for a fast pre-visualisation.

        self.Renderer.RemoveAllViewProps()
        Nodes = vtkPoints()
        for vertex in vertices:
            Nodes.InsertNextPoint(vertex.tolist())  

        Elements = vtkCellArray()
        for face in faces:
            idList = vtkIdList()
            for vertexIndex in face:
                idList.InsertNextId(vertexIndex)
            Elements.InsertNextCell(idList)

        Poly_Data = vtkPolyData()
        Poly_Data.SetPoints(Nodes)
        Poly_Data.SetPolys(Elements)
                
        Mapper = vtkPolyDataMapper()
        Mapper.SetInputData(Poly_Data)

        Actor = vtkActor()
        Actor.SetMapper(Mapper)
        Actor.GetProperty().SetColor(0, 1, 0)  
        self.Predefined_Camera()  
        self.Renderer.AddActor(Actor)
        self.Renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

        Grid = vtkCubeAxesActor()
        Grid.SetBounds(Poly_Data.GetBounds())  
        Grid.SetCamera(self.Renderer.GetActiveCamera())  
        Grid.GetXAxesGridlinesProperty().SetColor(0, 0, 0)  
        Grid.GetYAxesGridlinesProperty().SetColor(0, 0, 0)  
        Grid.GetZAxesGridlinesProperty().SetColor(0, 0, 0)  
        Grid.GetTitleTextProperty(0).SetColor(0.0, 0.0, 0.0)
        Grid.GetTitleTextProperty(1).SetColor(0.0, 0.0, 0.0)
        Grid.GetTitleTextProperty(2).SetColor(0.0, 0.0, 0.0)
        Grid.GetLabelTextProperty(0).SetColor(0, 0, 0)  
        Grid.GetLabelTextProperty(1).SetColor(0, 0, 0)  
        Grid.GetLabelTextProperty(2).SetColor(0, 0, 0)  
        Grid.GetXAxesLinesProperty().SetColor(0, 0, 0)
        Grid.GetYAxesLinesProperty().SetColor(0, 0, 0)
        Grid.GetZAxesLinesProperty().SetColor(0, 0, 0)
        Grid.DrawXGridlinesOn()
        Grid.DrawYGridlinesOn()
        Grid.DrawZGridlinesOn()
        Grid.SetGridLineLocation(Grid.VTK_GRID_LINES_FURTHEST)
        Grid.SetXLabelFormat("%6.4g")
        Grid.SetYLabelFormat("%6.4g")
        Grid.SetZLabelFormat("%6.4g")
        Grid.SetXAxisTickVisibility(True)
        Grid.SetYAxisTickVisibility(True)
        Grid.SetZAxisTickVisibility(True)

        self.Renderer.AddActor(Grid)
        self.Renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()  
        
    def Initialise_VTK_Components(self):
        
        # Load the VTK library components first for a faster loading when running for first time the application.
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.vtkDisplayWidget)

        Layout = QVBoxLayout(self.vtkDisplayWidget)
        Layout.setContentsMargins(1, 1, 1, 1)
        Layout.addWidget(self.vtkWidget)

        self.vtkDisplayWidget.setStyleSheet("QWidget { border: 1px solid black; }")

        self.Renderer = vtkRenderer()
        self.Renderer.SetBackground(1, 1, 1)  
        self.vtkWidget.GetRenderWindow().AddRenderer(self.Renderer)   
             
        self.Interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.Interactor.Initialize()
       
        self.Axes = vtkAxesActor()
        self.AxesWidget = vtkOrientationMarkerWidget()
        self.AxesWidget.SetOrientationMarker(self.Axes)
        self.AxesWidget.SetInteractor(self.Interactor)
        self.AxesWidget.SetViewport(0.0, 0.0, 0.3, 0.3) 
        self.AxesWidget.EnabledOn()
        self.AxesWidget.InteractiveOff()

        print("VTK compilation complete") 

    def Default_Model(self):
        
        # Generate a TPMS model when opening the app for first time. 
        
        self.Visibility(self.labelHeight, True)
        self.Visibility(self.lineEditHeight, True)
        self.Visibility(self.labelRadius, False)
        self.Visibility(self.lineEditRadius, False)

        Density = 0.3
        Length = 2  
        Radius = 2
        InnerRadius = 1
        Resolution = 80  
        NX, NY, NZ = 1, 1, 1  
        LX, LY, LZ = 1, 1, 1  

        XDomain, YDomain, ZDomain = Generate_Grid_Domain(Length, Resolution)
        KX, KY, KZ = Compute_Wave_Functions(NX, NY, NZ, LX, LY, LZ)
        Domain = Generate_3D_Domain("Cube", XDomain, YDomain, ZDomain, Length, Radius, InnerRadius)
        TPMS = Relative_Density("Primitive", Domain, "Sheet", Density, XDomain, YDomain, ZDomain, KX, KY, KZ)
        Vertices, Faces = Generate_Mesh(TPMS, Length, Resolution)

        self.Display_Mesh(Vertices, Faces)

    def Export(self):
        
        # Export generated mesh and select name and directory to save it.
        
        if self.meshData:
            
            Model_Mesh_Path, _ = QFileDialog.getSaveFileName(self, "Save TPMS mesh", "", "STL files (*.stl)", options=QFileDialog.Options())
            
            Pores_Mesh_Path = Model_Mesh_Path.replace(".stl", "_pores.stl")

            if Model_Mesh_Path:
                try:
                    
                    # Save TPMS mesh.
                    
                    Convert_STL(self.meshData['TPMS_Vertices'], self.meshData['TPMS_Faces'], Model_Mesh_Path)
                    
                    # Save Pores mesh.
                    
                    Convert_STL(self.meshData['Pores_Vertices'], self.meshData['Pores_Faces'], Pores_Mesh_Path)

                    QMessageBox.information(self, "Export successful", f"TPMS mesh saved to:\n{Model_Mesh_Path}\n\n pores mesh saved to:\n{Pores_Mesh_Path}")

                except Exception as e:
                    QMessageBox.critical(self, "Export failed", f"Failed to save the mesh: {e}")
            else:
                QMessageBox.warning(self, "Export cancelled", "Mesh export was cancelled.")
        else:
            self.Show_Error("No mesh to export. Please compute the mesh first.")
            
    def Compute(self):
        
        # Main function used to calculate and generate the TPMS model.
        
        try:
            
            NX = float(self.lineEditX.text())
            NY = float(self.lineEditY.text())
            NZ = float(self.lineEditZ.text())
            LX = float(self.lineEditLX.text())
            LY = float(self.lineEditLY.text())
            LZ = float(self.lineEditLZ.text()) 
            
            try:
                Length_Value = self.lineEditHeight.text()
                Radius_Value = self.lineEditRadius.text()
                Inner_Radius_Value = self.lineEditRadius_Inner.text()

                Length = float(Length_Value) if Length_Value else None
                Radius = float(Radius_Value) if Radius_Value else None
                InnerRadius = float(Inner_Radius_Value) if Inner_Radius_Value else None

                if Length is None and Radius is not None:
                    Length = Radius * 2.3
                elif Radius is None and Length is not None:
                    Radius = Length
                elif Length is None and Radius is None:
                    self.Show_Error("Both length and radius cannot be empty")
                    return 

            except ValueError as e:
                self.Show_Error(f"Invalid input value: {e}")
            except Exception as e:
                self.Show_Error(f"An unexpected error occurred: {e}")

            Resolution = int(self.lineEditResolution.text())
            Density = float(self.lineEditDensity.text())
            
            Tpms_Type = self.comboBoxEquation.currentText()
            Domain_Type = self.comboBoxDomain.currentText()
            Topology_Type = self.comboBoxTopology.currentText()
            Method_Type = self.comboBoxMethod.currentText()

            Length_Grid = None
            
            if Length/2 >= Radius:
                Length_Grid = Length
            else:
                Length_Grid = Radius*2
            
            if Domain_Type == "Cube":
                Bounds = (Length, Length, Length)

            elif Domain_Type == "Cuboid":
                Bounds = (Radius, Radius, Length)

            elif Domain_Type == "Sphere":
                Bounds = (2*Radius, 2*Radius, 2*Radius)

            elif Domain_Type == "Cylinder":
                Bounds = (2*Radius, 2*Radius, Length)

            elif Domain_Type == "Ring":
                Bounds = (2*Radius, 2*Radius, Length)
                
            XDomain, YDomain, ZDomain = Generate_Grid_Domain(Length_Grid, Resolution)
            KX, KY, KZ = Compute_Wave_Functions(NX, NY, NZ, LX, LY, LZ)
            Domain = Generate_3D_Domain(Domain_Type, XDomain, YDomain, ZDomain, Length, Radius, InnerRadius)
            
            if Method_Type == 'Relative Density':
                TPMS = Relative_Density(Tpms_Type, Domain, Topology_Type, Density, XDomain, YDomain, ZDomain, KX, KY, KZ)
            elif Method_Type == 'Constant Isovalue':
                TPMS = Isovalue_Mask(Tpms_Type, Domain, Topology_Type, Density, XDomain, YDomain, ZDomain, KX, KY, KZ)
    
            Vertices, Faces = Generate_Mesh(TPMS, Length_Grid, Resolution)
            Vertices, Faces = Map_Mesh(Vertices, Faces, Bounds)

            TPMS_Pores = - TPMS  
            
            Vertices_Pores, Faces_Pores = Generate_Mesh(TPMS_Pores, Length_Grid, Resolution)
            Vertices_Pores, Faces_Pores = Map_Mesh(Vertices_Pores, Faces_Pores, Bounds)

            self.meshData = {
                'TPMS_Vertices': Vertices,
                'TPMS_Faces': Faces,
                'Pores_Vertices': Vertices_Pores,
                'Pores_Faces': Faces_Pores
            }
            
            # Save the data mesh obtained.
                        
            PolyData = vtkPolyData()
            Points = vtkPoints()
            for vertex in Vertices:
                Points.InsertNextPoint(vertex.tolist())
            PolyData.SetPoints(Points)
            Cells = vtkCellArray()
            for face in Faces:
                idList = vtkIdList()
                for vertexIndex in face:
                    idList.InsertNextId(vertexIndex)
                Cells.InsertNextCell(idList)
            PolyData.SetPolys(Cells)
            
            self.Display_Mesh(Vertices, Faces)
            self.Mesh_Info(PolyData)
            
            Voxel_Size = np.divide(Length_Grid, (Resolution-1))
            
            # TPMS and pore topology statistics. 
            
            Pore_Analysis(TPMS, Voxel_Size)          
            Connectivity(TPMS, Domain, Voxel_Size)
            Curvature(Vertices, Faces)

        except ValueError as e:
            self.Show_Error(str(e))
    
################################################################################################
    
if __name__ == "__main__":
    app = QApplication.instance()  
    if not app:  
        app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())