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

# Recipe model import
from models.recipemodel import *

# Recipe dialogs import
from recipe import *

# Qt App declaration
app = QApplication(sys.argv)

class MainWindow(QWidget):
    # The main window class, inherits QWidget
    
    def enable_buttons(self):
        """
        Enables the Edit and Delete selected recipes buttons, two buttons that
        are disabled on startup because they require an item in the list to be
        selected before they can work.
        """
        self.editRecipeButton.setEnabled(True)
        self.deleteRecipeButton.setEnabled(True)

    def add_recipe(self):
        """
        Function that is called whenever the 'Add Recipe' button in the main
        screen has been clicked.

        Invokes an Add Recipe dialog, then catches its return value.
        """
        # Create a Recipe model to be passed to the dialog to be invoked
        recipe = RecipeModel() # create a recipe model
        addRecipeDialog = AddRecipeWindow(self)
        addRecipeDialog.exec_() # execute the dialog
        recipe = addRecipeDialog.get_recipe() # get the recipe from the dialog

        # Create a ShinyList item
        item = ShinyListItem()

        # Set shinylist text
        item.set_main_text(str(recipe.name))
        item.set_sub_text(recipe.course + ', serves ' +
                          str(recipe.servingSize))

        # Add the item to the shinylist
        self.recipeList.add_item(item)
        print 'Item added to shinylist'

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
        # Edit recipe button
        self.editRecipeButton = QPushButton("Edit Selected Recipe", self)
        # Delete recipe button
        self.deleteRecipeButton = QPushButton("Delete Selected Recipe", self)
        # We have to grey it out by default first because no recipe is
        # selected yet.
        self.deleteRecipeButton.setEnabled(False)
        # Same goes with the edit recipe button
        self.editRecipeButton.setEnabled(False)
        # Import Recipe button
        self.importRecipeButton = QPushButton("Import Recipes", self)
        # Export Recipe button
        self.exportRecipeButton = QPushButton("Export Recipe", self)
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
        self.rightHandLayout.addWidget(self.editRecipeButton)
        self.rightHandLayout.addWidget(self.deleteRecipeButton)
        self.rightHandLayout.addWidget(self.importRecipeButton)
        self.rightHandLayout.addWidget(self.exportRecipeButton)
        self.rightHandLayout.addWidget(self.generateShoppingListButton)

        # Initialize the buttons signals and slots
        self.addRecipeButton.clicked.connect(self.add_recipe)
        # Signal for when an item is clicked in the shinylist
        self.recipeList.clicked.connect(self.enable_buttons)

        self.show() # Show the window


    def __init__(self, parent=None):
        """
        Initialization function. Also calls the function that initializes
        the UI components.
        """
        # Initialize base class
        super(MainWindow, self).__init__(parent)

        # Variable to "announce" whether the system is ready to edit a recipe.
        self.edit_selected = 0

        print 'Initializing UI...' # some debug messages

        self.init_ui() # Initialize the ui
