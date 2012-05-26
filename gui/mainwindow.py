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
    
    def update_overview(self):
        """
        Updates the overview information (the data shown on the right hand
        side on top of the buttons) with the currently selected item on the
        list.
        """
        # Get the index of the currently selected item
        index = (self.recipeList.currentIndex()).row()

        # Update the values
        self.nameData.setText(self.recipes[index].name)
        self.courseData.setText(self.recipes[index].course)
        self.servingSizeData.setText(str(self.recipes[index].servingSize))

    def generate_shopping_list(self):
        """
        Invokes the dialog that generates a shopping list for the user.
        """
        # Get the index of the selected recipe
        index = (self.recipeList.currentIndex()).row()
        # Get the recipe based on that index
        recipe = self.recipes[index]

        # Create a shopping list dialog and pass the recipe to it
        generateShoppingListDialog = ShoppingListDialog(self, recipe)
        # Execute the dialog
        generateShoppingListDialog.exec_()

    def enable_buttons(self):
        """
        Enables the Edit and Delete selected recipes buttons, two buttons that
        are disabled on startup because they require an item in the list to be
        selected before they can work.

        Now also enables the Export Recipe button, because that also depends
        on a recipe being selected first.
        """
        self.editRecipeButton.setEnabled(True)
        self.deleteRecipeButton.setEnabled(True)
        self.exportRecipeButton.setEnabled(True)
        self.generateShoppingListButton.setEnabled(True)

        # Debug - print out index of current item in list
        print 'Selected: Index ' + str(self.recipeList.currentIndex().row())

    def disable_buttons(self):
        """
        Does the exact opposite of the function enable_buttons().
        """
        self.editRecipeButton.setEnabled(False)
        self.deleteRecipeButton.setEnabled(False)
        self.exportRecipeButton.setEnabled(False)
        self.generateShoppingListButton.setEnabled(False)

    def show_ingredient_overview(self):
        """
        Shows an overview of ingredients in a listwidget in the right hand
        side of the main layout.
        """
        # First we need to find the index of the first item in the list
        index = (self.recipeList.currentIndex()).row()

        # Remove all the current items in the list first
        self.ingredientsOverviewList.clear()

        # Show the ingredients of that recipe on the list.
        for ingredient in self.recipes[index].ingredients:
            # Loop through the list of ingredients for that recipe
            self.ingredientsOverviewList.addItem(str(ingredient[0]) + " - (" +
                    str(ingredient[1]) + " " + str(ingredient[2]) + ")")

    def show_instruction_overview(self):
        """
        Shows an overview of instructions in a listwidget in the right hand side
        of the main layout.
        """
        # Find the first item in the list
        index = (self.recipeList.currentIndex()).row()

        # Remove all the current items in the list first
        self.instructionsOverviewList.clear()

        # Create a counter variable
        counter = 1

        # Show the instructions of that recipe on the list
        for instruction in self.recipes[index].instructions:
            # Loop through the list of instructions for that recipe
            self.instructionsOverviewList.addItem(str(counter) + ". " +
                    instruction)
            counter += 1

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

    def edit_recipe(self):
        """
        A function that is called whenever the 'Edit Recipe' button in the
        main screen has been called, or an item is double clicked from the
        list.
        """
        # Create a recipe model
        recipe = RecipeModel()

        # Get the index of the recipe currently selected
        recipeIndex = self.recipeList.currentIndex()

        # Use the index to get the recipe from the list of recipes
        recipe = self.recipes[recipeIndex.row()]

        # Create a dialog and pass the selected recipe to it
        editRecipeDialog = EditRecipeWindow(self, recipe)
        if (editRecipeDialog.exec_()): # Exec the dialog
            # User pushed submit button

            # Get the recipe from the dialog
            recipe = editRecipeDialog.get_recipe()

            # Update the recipe in the list with the new one
            self.recipes[recipeIndex.row()] = recipe

            # Update the shinylist item
            self.shinyListItems[recipeIndex.row()].set_main_text(recipe.name)
            self.shinyListItems[recipeIndex.row()].set_sub_text(recipe.course +
                    ', serves ' + str(recipe.servingSize))

            # Refreshes the list
            self.refresh_list()

            # Disable the edit and delete recipe buttons again to "fool" the
            # user that their selection has been reset
            self.disable_buttons()

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

        # Overview of ingredients
        self.ingredientsOverviewLabel = QLabel("Ingredients Overview")
        self.ingredientsOverviewList = QListWidget()

        # Overview of instructions
        self.instructionsOverviewLabel = QLabel("Instructions Overview")
        self.instructionsOverviewList = QListWidget()

        # Add recipe button
        self.addRecipeButton = QPushButton("Add Recipe", self)
        # Edit recipe button
        self.editRecipeButton = QPushButton("Edit Selected Recipe", self)
        # Delete recipe button
        self.deleteRecipeButton = QPushButton("Delete Selected Recipe", self)
        # Import Recipe button
        self.importRecipeButton = QPushButton("Import Recipes", self)
        # Export Recipe button
        self.exportRecipeButton = QPushButton("Export Selected Recipe", self)
        # Generate Shopping List button
        self.generateShoppingListButton = QPushButton("Generate Shopping List",
                                                       self)

        # Disable the edit, delete, generate shopping list and export recipe
        # buttons because no recipe has been selected yet
        self.disable_buttons()

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

        # Add the overview of the ingredients and instructions for the
        # selected recipe
        self.rightHandLayout.addWidget(self.ingredientsOverviewLabel)
        self.rightHandLayout.addWidget(self.ingredientsOverviewList)
        self.rightHandLayout.addWidget(self.instructionsOverviewLabel)
        self.rightHandLayout.addWidget(self.instructionsOverviewList)

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
        self.recipeList.clicked.connect(self.update_overview)
        self.recipeList.clicked.connect(self.show_ingredient_overview)
        self.recipeList.clicked.connect(self.show_instruction_overview)
        # Signal when an item is double-clicked
        self.recipeList.doubleClicked.connect(self.edit_recipe)
        # Signal to edit a recipe when the edit recipe button is clicked
        self.editRecipeButton.clicked.connect(self.edit_recipe)
        # Signal to delete a recipe when the delete recipe button is clicked
        self.deleteRecipeButton.clicked.connect(self.delete_recipe)
        # Signal to import a recipe
        self.importRecipeButton.clicked.connect(self.import_recipe)
        # Signal to export a recipe
        self.exportRecipeButton.clicked.connect(self.export_recipe)
        # Signal to invoke the shopping list dialog when the generate shopping
        # list button is clicked
        self.generateShoppingListButton.clicked.connect(
                self.generate_shopping_list)

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
