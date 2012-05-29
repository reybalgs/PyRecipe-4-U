###############################################################################
#
# mainwindow.py
#
# The mainwindow of the GUI. Displays overview recipe information, plus other
# functionalities.
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
                              str(recipe.servingSize))

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
        fileDialog = QFileDialog(self)
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

            # Create a "raw" recipe object from the file
            raw_recipe = json.loads(file.read())

            # Set the name of the recipe
            recipe.name = raw_recipe[0]['name']
            # Set the course of the recipe
            recipe.course = raw_recipe[1]['course']
            # Set the serving size of the recipe
            recipe.servingSize = float(raw_recipe[2]['serving_size'])
            # Set the ingredients of the recipe
            for ingredient in raw_recipe[3]['ingredients']:
                recipe.ingredients.append([ingredient[0], ingredient[1], 
                                           ingredient[2]])

            # Set the instructions of the recipe
            for instruction in raw_recipe[4]['instructions']:
                recipe.instructions.append(instruction)

            # Create a shinylist item
            item = ShinyListItem()

            # Set the main and subtext of the shinylist item
            item.set_main_text(recipe.name)
            item.set_sub_text(recipe.course + ', serves ' +
                              str(recipe.servingSize))

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

        # Encode the recipe into a JSON string
        json_recipe = json.dumps([{"name":recipe.name},
            {"course":recipe.course}, {"serving_size":recipe.servingSize},
            {"ingredients":recipe.ingredients},
            {"instructions":recipe.instructions}])

        # Create a filedialog for saving the file
        fileDialog = QFileDialog(self)
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

    def open_recipe(self):
        """
        Opens up a concise and detailed dialog containing essential
        information about the double-clicked recipe.
        """
        # Get the index of the selected recipe
        index = self.recipeList.currentIndex().row()

        # Get the recipe based on that index
        recipe = self.recipes[index]

        # Create a recipe overview dialog, pass the recipe to it
        recipeDialog = RecipeOverview(self, recipe)
        # Execute that dialog
        recipeDialog.exec_()

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

        # Layouting
        # Time to link together the different UI components
        self.setLayout(self.mainLayout) # set the main layout

        # Put the shinylist in the main layout
        self.mainLayout.addWidget(self.recipeList)

        # Put the button layout in the main layout
        self.mainLayout.addLayout(self.buttonLayout)

        # Put the buttons in the button layout
        self.buttonLayout.addWidget(self.addRecipeButton)
        self.buttonLayout.addWidget(self.deleteRecipeButton)
        self.buttonLayout.addWidget(self.importRecipeButton)
        self.buttonLayout.addWidget(self.exportRecipeButton)
        
        # Initialize the buttons signals and slots
        self.addRecipeButton.clicked.connect(self.add_recipe)
        # Signal for when an item is clicked in the shinylist
        self.recipeList.clicked.connect(self.enable_buttons)
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
        # Create a list of shinylist items
        self.shinyListItems = []
