# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIDefinitive.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(818, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelLogo = QLabel(self.centralwidget)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setGeometry(QRect(540, 280, 201, 161))
        self.labelLogo.setPixmap(QPixmap(u"logo_m2be_2024.png"))
        self.labelLogo.setScaledContents(True)
        self.vtkDisplayWidget = QWidget(self.centralwidget)
        self.vtkDisplayWidget.setObjectName(u"vtkDisplayWidget")
        self.vtkDisplayWidget.setGeometry(QRect(490, 20, 301, 251))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(70, 320, 361, 122))
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelResolution = QLabel(self.layoutWidget)
        self.labelResolution.setObjectName(u"labelResolution")
        font = QFont()
        font.setBold(True)
        self.labelResolution.setFont(font)

        self.gridLayout.addWidget(self.labelResolution, 0, 0, 1, 1)

        self.lineEditResolution = QLineEdit(self.layoutWidget)
        self.lineEditResolution.setObjectName(u"lineEditResolution")
        self.lineEditResolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEditResolution, 0, 1, 1, 1)

        self.pushButtonDisplay = QPushButton(self.layoutWidget)
        self.pushButtonDisplay.setObjectName(u"pushButtonDisplay")

        self.gridLayout.addWidget(self.pushButtonDisplay, 0, 2, 1, 1)

        self.labelResolution_2 = QLabel(self.layoutWidget)
        self.labelResolution_2.setObjectName(u"labelResolution_2")
        self.labelResolution_2.setFont(font)

        self.gridLayout.addWidget(self.labelResolution_2, 1, 0, 1, 1)

        self.lineEditDensity = QLineEdit(self.layoutWidget)
        self.lineEditDensity.setObjectName(u"lineEditDensity")
        self.lineEditDensity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEditDensity, 1, 1, 1, 1)

        self.pushButtonExport = QPushButton(self.layoutWidget)
        self.pushButtonExport.setObjectName(u"pushButtonExport")

        self.gridLayout.addWidget(self.pushButtonExport, 1, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelContact = QLabel(self.layoutWidget)
        self.labelContact.setObjectName(u"labelContact")
        self.labelContact.setFont(font)

        self.gridLayout_2.addWidget(self.labelContact, 0, 0, 2, 1)

        self.labelMail1 = QLabel(self.layoutWidget)
        self.labelMail1.setObjectName(u"labelMail1")

        self.gridLayout_2.addWidget(self.labelMail1, 0, 1, 1, 1)

        self.labelMail2 = QLabel(self.layoutWidget)
        self.labelMail2.setObjectName(u"labelMail2")

        self.gridLayout_2.addWidget(self.labelMail2, 1, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(80, 20, 331, 140))
        self.gridLayout_4 = QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.labelDomain = QLabel(self.layoutWidget1)
        self.labelDomain.setObjectName(u"labelDomain")
        self.labelDomain.setFont(font)
        self.labelDomain.setScaledContents(False)
        self.labelDomain.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelDomain, 0, 0, 1, 1)

        self.comboBoxDomain = QComboBox(self.layoutWidget1)
        self.comboBoxDomain.setObjectName(u"comboBoxDomain")

        self.gridLayout_4.addWidget(self.comboBoxDomain, 0, 1, 1, 1)

        self.labelEquation = QLabel(self.layoutWidget1)
        self.labelEquation.setObjectName(u"labelEquation")
        self.labelEquation.setFont(font)
        self.labelEquation.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelEquation, 1, 0, 1, 1)

        self.comboBoxEquation = QComboBox(self.layoutWidget1)
        self.comboBoxEquation.setObjectName(u"comboBoxEquation")
        self.comboBoxEquation.setEditable(False)

        self.gridLayout_4.addWidget(self.comboBoxEquation, 1, 1, 1, 1)

        self.labelTopology = QLabel(self.layoutWidget1)
        self.labelTopology.setObjectName(u"labelTopology")
        self.labelTopology.setFont(font)
        self.labelTopology.setScaledContents(False)
        self.labelTopology.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelTopology, 2, 0, 1, 1)

        self.comboBoxTopology = QComboBox(self.layoutWidget1)
        self.comboBoxTopology.setObjectName(u"comboBoxTopology")

        self.gridLayout_4.addWidget(self.comboBoxTopology, 2, 1, 1, 1)

        self.labelMethod = QLabel(self.layoutWidget1)
        self.labelMethod.setObjectName(u"labelMethod")
        self.labelMethod.setFont(font)
        self.labelMethod.setScaledContents(False)
        self.labelMethod.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelMethod, 3, 0, 1, 1)

        self.comboBoxMethod = QComboBox(self.layoutWidget1)
        self.comboBoxMethod.setObjectName(u"comboBoxMethod")

        self.gridLayout_4.addWidget(self.comboBoxMethod, 3, 1, 1, 1)

        self.layoutWidget2 = QWidget(self.centralwidget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(30, 170, 441, 137))
        self.gridLayout_9 = QGridLayout(self.layoutWidget2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lineEditRadius = QLineEdit(self.layoutWidget2)
        self.lineEditRadius.setObjectName(u"lineEditRadius")
        self.lineEditRadius.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEditRadius, 1, 1, 1, 1)

        self.labelRadius = QLabel(self.layoutWidget2)
        self.labelRadius.setObjectName(u"labelRadius")

        self.gridLayout_7.addWidget(self.labelRadius, 1, 0, 1, 1)

        self.labelHeight = QLabel(self.layoutWidget2)
        self.labelHeight.setObjectName(u"labelHeight")

        self.gridLayout_7.addWidget(self.labelHeight, 3, 0, 1, 1)

        self.lineEditHeight = QLineEdit(self.layoutWidget2)
        self.lineEditHeight.setObjectName(u"lineEditHeight")
        self.lineEditHeight.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEditHeight, 3, 1, 1, 1)

        self.labelGeometryParameters = QLabel(self.layoutWidget2)
        self.labelGeometryParameters.setObjectName(u"labelGeometryParameters")
        self.labelGeometryParameters.setFont(font)

        self.gridLayout_7.addWidget(self.labelGeometryParameters, 0, 0, 1, 2)

        self.labelRadius_Inner = QLabel(self.layoutWidget2)
        self.labelRadius_Inner.setObjectName(u"labelRadius_Inner")

        self.gridLayout_7.addWidget(self.labelRadius_Inner, 2, 0, 1, 1)

        self.lineEditRadius_Inner = QLineEdit(self.layoutWidget2)
        self.lineEditRadius_Inner.setObjectName(u"lineEditRadius_Inner")
        self.lineEditRadius_Inner.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEditRadius_Inner, 2, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.labelUnitCellsNumber = QLabel(self.layoutWidget2)
        self.labelUnitCellsNumber.setObjectName(u"labelUnitCellsNumber")
        self.labelUnitCellsNumber.setFont(font)
        self.labelUnitCellsNumber.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.labelUnitCellsNumber, 0, 0, 1, 2)

        self.labelX = QLabel(self.layoutWidget2)
        self.labelX.setObjectName(u"labelX")

        self.gridLayout_6.addWidget(self.labelX, 1, 0, 1, 1)

        self.lineEditX = QLineEdit(self.layoutWidget2)
        self.lineEditX.setObjectName(u"lineEditX")
        self.lineEditX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEditX, 1, 1, 1, 1)

        self.labelY = QLabel(self.layoutWidget2)
        self.labelY.setObjectName(u"labelY")

        self.gridLayout_6.addWidget(self.labelY, 2, 0, 1, 1)

        self.lineEditY = QLineEdit(self.layoutWidget2)
        self.lineEditY.setObjectName(u"lineEditY")
        self.lineEditY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEditY, 2, 1, 1, 1)

        self.labelZ = QLabel(self.layoutWidget2)
        self.labelZ.setObjectName(u"labelZ")

        self.gridLayout_6.addWidget(self.labelZ, 3, 0, 1, 1)

        self.lineEditZ = QLineEdit(self.layoutWidget2)
        self.lineEditZ.setObjectName(u"lineEditZ")
        self.lineEditZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEditZ, 3, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.labelUnitCellsLength = QLabel(self.layoutWidget2)
        self.labelUnitCellsLength.setObjectName(u"labelUnitCellsLength")
        self.labelUnitCellsLength.setFont(font)
        self.labelUnitCellsLength.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.labelUnitCellsLength, 0, 0, 1, 2)

        self.labelLX = QLabel(self.layoutWidget2)
        self.labelLX.setObjectName(u"labelLX")

        self.gridLayout_5.addWidget(self.labelLX, 1, 0, 1, 1)

        self.lineEditLX = QLineEdit(self.layoutWidget2)
        self.lineEditLX.setObjectName(u"lineEditLX")
        self.lineEditLX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEditLX, 1, 1, 1, 1)

        self.labeLY = QLabel(self.layoutWidget2)
        self.labeLY.setObjectName(u"labeLY")

        self.gridLayout_5.addWidget(self.labeLY, 2, 0, 1, 1)

        self.lineEditLY = QLineEdit(self.layoutWidget2)
        self.lineEditLY.setObjectName(u"lineEditLY")
        self.lineEditLY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEditLY, 2, 1, 1, 1)

        self.labelLZ = QLabel(self.layoutWidget2)
        self.labelLZ.setObjectName(u"labelLZ")

        self.gridLayout_5.addWidget(self.labelLZ, 3, 0, 1, 1)

        self.lineEditLZ = QLineEdit(self.layoutWidget2)
        self.lineEditLZ.setObjectName(u"lineEditLZ")
        self.lineEditLZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEditLZ, 3, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_5, 0, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 818, 43))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelLogo.setText("")
        self.labelResolution.setText(QCoreApplication.translate("MainWindow", u"Select Resolution Value:", None))
        self.pushButtonDisplay.setText(QCoreApplication.translate("MainWindow", u"Display", None))
        self.labelResolution_2.setText(QCoreApplication.translate("MainWindow", u"Select Relative Density: ", None))
        self.pushButtonExport.setText(QCoreApplication.translate("MainWindow", u"Export STL", None))
        self.labelContact.setText(QCoreApplication.translate("MainWindow", u"Contact Information: ", None))
        self.labelMail1.setText(QCoreApplication.translate("MainWindow", u"pablo.martin@unizar.es", None))
        self.labelMail2.setText(QCoreApplication.translate("MainWindow", u"angeles@unizar.es", None))
        self.labelDomain.setText(QCoreApplication.translate("MainWindow", u"Select 3D Domain:", None))
        self.labelEquation.setText(QCoreApplication.translate("MainWindow", u"Select TPMS Equation:", None))
        self.labelTopology.setText(QCoreApplication.translate("MainWindow", u"Select Topology:", None))
        self.labelMethod.setText(QCoreApplication.translate("MainWindow", u"Select Method:", None))
        self.labelRadius.setText(QCoreApplication.translate("MainWindow", u"ExRadius:", None))
        self.labelHeight.setText(QCoreApplication.translate("MainWindow", u"Length:", None))
        self.labelGeometryParameters.setText(QCoreApplication.translate("MainWindow", u"Geometry Parameters:", None))
        self.labelRadius_Inner.setText(QCoreApplication.translate("MainWindow", u"InRadius:", None))
        self.labelUnitCellsNumber.setText(QCoreApplication.translate("MainWindow", u"Number of Unit Cells:", None))
        self.labelX.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.labelY.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.labelZ.setText(QCoreApplication.translate("MainWindow", u"Z:", None))
        self.labelUnitCellsLength.setText(QCoreApplication.translate("MainWindow", u"Unit Cells Length:", None))
        self.labelLX.setText(QCoreApplication.translate("MainWindow", u"LX:", None))
        self.labeLY.setText(QCoreApplication.translate("MainWindow", u"LY:", None))
        self.labelLZ.setText(QCoreApplication.translate("MainWindow", u"LZ:", None))
    # retranslateUi

