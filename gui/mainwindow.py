###############################################################################
#
# mainwindow.py
#
# The mainwindow of the GUI. The GUI will probably only have one window anyway,
# for minimalism.
#
###############################################################################

import sys # for system calls we might need

# Pyside imports
from PySide.QtCore import *
from PySide.QtGui import *

# Shinylist import
from shinylist import *

# Qt App declaration
app = QApplication(sys.argv)

class MainWindow(QWidget):
    # The main window class, inherits QWidget
    def init_ui(self):
        """
        Function that initializes the UI components of the app.
        Only initialization is done here.
        """
        # Creation
        # Creates UI components, but does not link them together yet.

        self.mainLayout = QVBoxLayout() # main layout
        self.splitViewLayout = QHBoxLayout() # splitting layout

        # Create the shinylist
        self.recipeList = ShinyList()

        self.recipeOverviewLayout = QFormLayout() # layout for recipe overview
        self.rightHandLayout = QVBoxLayout() # layout for the right hand side

        # label above the recipeOverviewLayout
        self.recipeOverviewTitle = QLabel("Recipe Information")
        
        # where name data is displayed
        self.nameData = QLabel("Select recipe from list first")
        # where the course data is displayed
        self.courseData = QLabel("Select recipe from list first")
        # where the serving size data is displayed
        self.servingSizeData = QLabel("Select recipe from list first")

        # Add recipe button
        self.addRecipeButton = QPushButton("Add Recipe", self)
        # Delete recipe button
        self.deleteRecipeButton = QPushButton("Delete Recipe", self)
        # We have to grey it out by default first because no recipe is
        # selected yet.
        self.deleteRecipeButton.setEnabled(False)
        # Generate Shopping List button
        self.generateShoppingListButton = QPushButton("Generate Shopping List",
                                                       self)

        # Layouting
        # Time to link together the different UI components
        self.setLayout(self.mainLayout) # set the main layout
        # Add the split view layout to the main layout
        self.mainLayout.addLayout(self.splitViewLayout)
        
        # Add the table to the split layout, being the first, it's
        # automatically put to the left.
        self.splitViewLayout.addWidget(self.recipeList)
        # Add the right hand layout to the split layout.
        self.splitViewLayout.addLayout(self.rightHandLayout)
        
        # Add the Recipe Information label to the right hand layout.
        self.rightHandLayout.addWidget(self.recipeOverviewTitle)
        # Add the recipe overview form layout to the right hand layout.
        self.rightHandLayout.addLayout(self.recipeOverviewLayout)

        # Add the elements of the recipe overview form layout to itself
        self.recipeOverviewLayout.addRow("Name:", self.nameData)
        self.recipeOverviewLayout.addRow("Course:", self.courseData)
        self.recipeOverviewLayout.addRow("Serving Size:", self.servingSizeData)

        # Add a stretching spacer to separate the overview and the buttons
        self.rightHandLayout.addStretch()
        # Add the three buttons into the layout
        self.rightHandLayout.addWidget(self.addRecipeButton)
        self.rightHandLayout.addWidget(self.deleteRecipeButton)
        self.rightHandLayout.addWidget(self.generateShoppingListButton)

        self.show() # Show the window


    def __init__(self, parent=None):
        """
        Initialization function. Also calls the function that initializes
        the UI components.
        """
        # Initialize base class
        super(MainWindow, self).__init__(parent)

        print 'Initializing UI...' # some debug messages

        self.init_ui() # Initialize the ui
