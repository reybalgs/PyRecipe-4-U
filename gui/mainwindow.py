###############################################################################
#
# mainwindow.py
#
# The mainwindow of the GUI. Displays overview recipe information, and recipe
# details.
#
###############################################################################

import sys # for system calls we might need
import simplejson as json # for JSON decoding and encoding

# Pyside imports
from PySide.QtCore import *
from PySide.QtGui import *

# Shinylist import
from shinylist import *

# Recipe model import
from models.recipemodel import *

# Recipe dialogs import
from recipe import *

# Generate shopping list dialog import
from shopping_list import *

# Qt App declaration
app = QApplication(sys.argv)

class MainWindow(QWidget):
    # The main window class, inherits QWidget
    def refresh_ingredients(self):
        """
        Refreshes the list of ingredients for the current selected recipe.
        """
        self.ingredientsData.clear() # clear the list first
        
        counter = 1 # Counter variable

        # Put the text in the ingredients list
        for ingredient in self.recipes[self.currentRecipe].ingredients:
            # Go through the list of ingredients
            self.ingredientsData.insertPlainText(str(counter) + '. ' +
                    ingredient['name'] + ': ' + str(ingredient['quantity']) +
                    ' ' + ingredient['unit'] + '\n')
            counter += 1

    def refresh_instructions(self):
        """
        Refreshes the list of instructions for the current selected recipe.
        """
        self.instructionsData.clear() # clear the list

        counter = 1 # Counter variable

        # Put text in the instructions list
        for instruction in self.recipes[self.currentRecipe].instructions:
            # Go through the list of instructions
            self.instructionsData.insertPlainText(str(counter) + '. ' +
                instruction + '\n')
            counter += 1

    def enable_buttons(self):
        """
        Enables the Edit and Delete selected recipes buttons, two buttons that
        are disabled on startup because they require an item in the list to be
        selected before they can work.

        Now also enables the Export Recipe button, because that also depends
        on a recipe being selected first.
        """
        self.deleteRecipeButton.setEnabled(True)
        self.exportRecipeButton.setEnabled(True)

    def disable_buttons(self):
        """
        Does the exact opposite of the function enable_buttons().
        """
        self.deleteRecipeButton.setEnabled(False)
        self.exportRecipeButton.setEnabled(False)

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

        if not ((recipe.name == 'noname' or recipe.name == '') and 
                recipe.servingSize == 0.0):
            # We got a proper recipe, carry on
            # Create a ShinyList item
            item = ShinyListItem()

            # Set shinylist text
            item.set_main_text(str(recipe.name))
            item.set_sub_text(recipe.course + ', serves ' +
                              str(recipe.servingSize) + ' people')

            # Add the item to the shinylist
            self.recipeList.add_item(item)
            print 'Item added to shinylist'

            # Add the item to the list of shinylist items
            self.shinyListItems.append(item)

            # Add the recipe to the list of recipes
            self.recipes.append(recipe)

    def import_recipe(self):
        """
        Imports a recipe file (.rcpe) from a directory in the user's filesystem
        and then adds it to the current list of recipes.
        """
        # Create a recipe object
        recipe = RecipeModel()
        # Invoke a filedialog that will look for the .rcpe file
        fileDialog = QFileDialog(self, "Import Recipe", "./recipes/")
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setNameFilter("Recipe File(*.rcpe)")
        
        # An empty file location
        file = None
        filePath = '' # Initialize an empty filepath
        if fileDialog.exec_():
            filePath = fileDialog.selectedFiles()
            print filePath

        if (filePath):
            # There is a file, so let's continue on
            # Read from the filepath
            file = open(filePath[0], 'r')

            # Load the file into the recipe
            recipe.import_recipe(file.read())

            # Create a shinylist item
            item = ShinyListItem()

            # Set the main and subtext of the shinylist item
            item.set_main_text(recipe.name)
            item.set_sub_text(recipe.course + ', serves ' +
                              str(recipe.servingSize) + ' people')

            # Add the item to the shinylist
            self.recipeList.add_item(item)
            # and to the list of shinylist items as well
            self.shinyListItems.append(item)

            # Add the recipe to the list of recipes
            self.recipes.append(recipe)

            # Close the file
            file.close()

    def export_recipe(self):
        """
        Exports the selected recipe in the list as a recipe file (.rcpe).
        """
        # Get the index of the current recipe selected
        index = (self.recipeList.currentIndex()).row()

        # Get the recipe from the list of recipes using that index
        recipe = self.recipes[index]
    
        # Print the recipe first (debug)
        recipe.print_recipe_information()

        # Encode the recipe into a JSON string
        json_recipe = recipe.export_recipe()

        # Create a filedialog for saving the file
        fileDialog = QFileDialog(self, "Export Recipe", "./recipes/")
        fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setNameFilter("Recipe File(*.rcpe)")
        fileDialog.setDefaultSuffix("rcpe")

        # Initialize an empty file path
        filePath = ''
        # Execute the dialog
        if fileDialog.exec_():
            filePath = fileDialog.selectedFiles()

        if (filePath):
            # There's a valid filepath, so let's continue
            # Open the file for writing
            file = open(filePath[0], 'w')

            # Write the JSON string into the file
            file.write(json_recipe)

            # Close the file
            file.close()

            # Open the file again for reading
            file = open(filePath[0], 'r')
            print file.read()
            file.close()

    def refresh_recipe_info(self):
        """
        Refreshes the recipe details displayed according to the current recipe
        variable
        """
        self.nameData.setText(self.recipes[self.currentRecipe].name)
        # Set the course data according to the recipe's course data
        if(self.recipes[self.currentRecipe].course == 'Appetizer'):
            self.courseData.setCurrentIndex(0)
        elif(self.recipes[self.currentRecipe].course == 'Main'):
            self.courseData.setCurrentIndex(1)
        elif(self.recipes[self.currentRecipe].course == 'Dessert'):
            self.courseData.setCurrentIndex(2)
        else:
            print('Error! Wrong course data in recipe!')
        self.servingSizeData.setValue(
                self.recipes[self.currentRecipe].servingSize)

        self.refresh_ingredients()
        self.refresh_instructions()

    def open_recipe(self):
        """
        """
        # Get the index of the selected recipe
        index = self.recipeList.currentIndex().row()

        # Get the recipe based on that index
        recipe = self.recipes[index]

        # Get the recipe from the dialog
        recipe = recipeDialog.get_recipe()
        self.recipes[index] = recipe

        # Update the shinylist item the recipe is referred to
        self.shinyListItems[index].set_main_text(recipe.name)
        self.shinyListItems[index].set_sub_text(recipe.course + ', serves ' +
                str(recipe.servingSize) + ' people')

        # Refresh the list of recipes
        self.refresh_list()

    def refresh_list(self):
        """
        Deletes the entire shinylist and then repopulates it using the list
        of shinylist items.
        """
        # Clear the entire shinylist
        self.recipeList.clear()

        # Repopulate the shinylist
        for item in self.shinyListItems:
            self.recipeList.add_item(item)

    def delete_recipe(self):
        """
        The function that is in charge of deleting recipes from the
        application's list of recipes. Once a recipe is deleted, it is
        irreversible, unless the user has exported that recipe previously.
        """
        # First we get the index of the recipe we are going to delete
        recipeIndex = (self.recipeList.currentIndex()).row()

        # Delete that recipe from the list of recipes (non-visible list)
        self.recipes.pop(recipeIndex)

        # Delete that recipe from the list of recipes (shinylist)
        self.shinyListItems.pop(recipeIndex)

        # Reinitialize the list
        self.refresh_list()

        # Disable the buttons that have to be disabled
        self.disable_buttons()

    def init_ui(self):
        """
        Function that initializes the UI components of the app.
        Only initialization is done here.
        """
        # Creation
        # Creates UI components, but does not link them together yet.
        
        self.mainLayout = QVBoxLayout() # main layout
        self.buttonLayout = QHBoxLayout() # hor layout for buttons
        self.columnLayout = QHBoxLayout() # Hor layout for most of the stuff
        self.listLayout = QVBoxLayout() # Layout for the list on the left

        # Create the menu bar
        self.menuBar = QMenuBar(self)
        # Create the different menus
        self.fileMenu = QMenu("File", self)
        self.editMenu = QMenu("Edit", self)
        self.helpMenu = QMenu("Help", self)
        # Add some basic actions for the menu bar. They don't do anything yet.
        # TODO: Make these actions actually do something.
        self.fileMenu.addAction("New Recipe")
        self.fileMenu.addAction("Import Recipe")
        self.fileMenu.addAction("Export Recipe")
        self.fileMenu.addAction("Delete Recipe")
        self.fileMenu.addAction("Exit")
        self.editMenu.addAction("Details")
        self.editMenu.addAction("Ingredients")
        self.editMenu.addAction("Instructions")
        self.helpMenu.addAction("About PyRecipe4U")
        # Add the menus to the menu bar
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.editMenu)
        self.menuBar.addMenu(self.helpMenu)

        # Main components
        # Create the shinylist
        self.recipeList = ShinyList()
        # Tooltip for the shinylist
        self.recipeList.setToolTip("Double-click a recipe to view and edit " +
                "its contents.")

        # Add recipe button
        self.addRecipeButton = QPushButton("Add", self)
        # Tooltip for add recipe
        self.addRecipeButton.setToolTip("Create and add a new " +
                "recipe into the database.")
        # Delete recipe button
        self.deleteRecipeButton = QPushButton("Delete", self)
        # Tooltip for delete recipe
        self.deleteRecipeButton.setToolTip("Deletes the selected " +
                "recipe from the database.")
        # Import Recipe button
        self.importRecipeButton = QPushButton("Import", self)
        # Tooltip for import recipe
        self.importRecipeButton.setToolTip("Loads a .rcpe recipe " +
                "file from your filesystem.")
        # Export Recipe button
        self.exportRecipeButton = QPushButton("Export", self)
        # Tooltip for export recipe
        self.exportRecipeButton.setToolTip("Saves the selected " +
                "recipe to a .rcpe recipe file on your filesystem.")

        # Disable the edit, delete, generate shopping list and export recipe
        # buttons because no recipe has been selected yet
        self.disable_buttons()

        ######################################################################
        # Recipe overview items
        ######################################################################
        # Layouts
        self.recipeOverviewLayout = QGridLayout()
        
        # Items and labels
        self.nameData = QLineEdit(self)
        self.courseData = QComboBox()
        self.courseData.insertItem(0, "Appetizer")
        self.courseData.insertItem(1, "Main")
        self.courseData.insertItem(2, "Dessert")
        self.servingSizeData = QDoubleSpinBox(self)
        self.ingredientsData = QTextBrowser()
        self.instructionsData = QTextBrowser()

        # Layouting
        # Time to link together the different UI components
        self.setLayout(self.mainLayout) # set the main layout

        # Put the menubar in the main layout
        self.mainLayout.addWidget(self.menuBar)

        # Put the column layout in the main layout
        self.mainLayout.addLayout(self.columnLayout)

        # Put the list layout in the first slot of the column layout
        self.columnLayout.addLayout(self.listLayout)

        # Put the recipe overview layout in the second slot of the column
        # layout
        self.columnLayout.addLayout(self.recipeOverviewLayout)

        # Put the items and labels of a recipe into the recipe overview grid
        # layout
        self.recipeOverviewLayout.addWidget(QLabel("Recipe Name:"),
                0, 0)
        self.recipeOverviewLayout.addWidget(self.nameData, 0, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Course:"), 1, 0)
        self.recipeOverviewLayout.addWidget(self.courseData, 1, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Serving Size:"), 2, 0)
        self.recipeOverviewLayout.addWidget(self.servingSizeData, 2, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Ingredients:"), 3, 0)
        self.recipeOverviewLayout.addWidget(self.ingredientsData, 3, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Instructions:"), 4, 0)
        self.recipeOverviewLayout.addWidget(self.instructionsData, 4, 1)

        # Put the shinylist in the list layout
        self.listLayout.addWidget(self.recipeList)

        # Put the button layout in the list layout
        self.listLayout.addLayout(self.buttonLayout)

        # Put the buttons in the button layout
        self.buttonLayout.addWidget(self.addRecipeButton)
        self.buttonLayout.addWidget(self.deleteRecipeButton)
        self.buttonLayout.addWidget(self.importRecipeButton)
        self.buttonLayout.addWidget(self.exportRecipeButton)
        
        # Initialize the buttons signals and slots
        self.addRecipeButton.clicked.connect(self.add_recipe)
        # Signal for when an item is clicked in the shinylist
        self.recipeList.clicked.connect(self.enable_buttons)
        self.recipeList.clicked.connect(self.refresh_recipe_info)
        # Signal when an item is double-clicked
        self.recipeList.doubleClicked.connect(self.open_recipe)
        # Signal to delete a recipe when the delete recipe button is clicked
        self.deleteRecipeButton.clicked.connect(self.delete_recipe)
        # Signal to import a recipe
        self.importRecipeButton.clicked.connect(self.import_recipe)
        # Signal to export a recipe
        self.exportRecipeButton.clicked.connect(self.export_recipe)

        # Set the window title
        self.setWindowTitle("PyRecipe-4-U")
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

        # Create list of recipes
        self.recipes = []
        # A variable to track the current recipe selected
        self.currentRecipe = 0
        # Create a list of shinylist items
        self.shinyListItems = []
