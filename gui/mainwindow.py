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

# Ingredients window import
from ingredients import *

# Instructions window import
from instructions import *

# Qt App declaration
app = QApplication(sys.argv)

class MainWindow(QWidget):
    # The main window class, inherits QWidget
    def clear_data(self):
        """
        Clears the data fields.
        """
        self.nameData.setText("")
        self.courseData.setCurrentIndex(-1)
        self.servingSizeData.setValue(0.0)
        self.ingredientsData.clear()
        self.instructionsData.clear()
        
    def shinylist_click(self):
        """
        SLOT function called whenever an item is clicked on the shinylist.
        Calls the two other functions.
        """
        self.refresh_current_recipe()
        self.refresh_recipe_info()
        self.refresh_image()

    def refresh_current_recipe(self):
        """
        Updates the current recipe selected according to the item selected by
        the user
        """
        # Get the currently selected item from the shinylist and put it in the
        # tracking variable
        self.currentRecipe = (self.recipeList.currentIndex()).row()

    def edit_instructions(self):
        """
        Invokes the edit instructions window, where the user can edit the
        instructions of the currently selected recipe
        """
        # Create the dialog
        instructionsDialog = InstructionsWindow(self,
                self.recipes[self.currentRecipe].instructions)

        # Execute the dialog
        instructionsDialog.exec_()

        # Get the updated list of instructions from the dialog
        self.recipes[self.currentRecipe].instructions = instructionsDialog.get_instructions()

        # Refresh the list of instructions
        self.refresh_instructions()

    def next_image(self):
        """
        Moves to the next image in the recipe's array of images.
        """
        if len(self.recipes[self.currentRecipe].images) > 1:
            # The recipe has images to go to
            if (self.currentRecipe < 
                    (len(self.recipes[self.currentRecipe].images) - 1)):
                # We are not at the end of the list, we can move forward
                # Increment the selected image variable
                self.currentImage += 1
                # Change the displayed image
                self.refresh_image()
            else:
                print('Already at the end of images list')

    def previous_image(self):
        """
        Moves to the previous image in the recipe's array of images.
        """
        if len(self.recipes[self.currentRecipe].images) > 1:
            # The recipe has images to go to
            if self.currentImage > 0:
                # We are not at the beginning of the image list so we can move
                # back at least once
                # Decrement the selected image
                self.currentImage -= 1
                # Change the displayed image
                self.refresh_image()
            else:
                print('Already at the beginning of the list!')

    def import_image(self):
        """
        Imports a new image for the currently selected recipe
        """
        # A var containing a list of images
        files = ''
        # Invoke a filedialog that will look for the images
        fileDialog = QFileDialog(self, "Import Image", "./gui/images")
        fileDialog.setFileMode(QFileDialog.ExistingFile)

        if fileDialog.exec_():
            # Get the selected files from the dialog
            files = fileDialog.selectedFiles()

        # Now let's loop through the list of files and put them into the list
        # of images
        for image in files:
            if ((image) and (image.lower().endswith(('.png', '.jpg', '.jpeg',
                    '.gif', '.bmp')))):
                # There is an image found, add it to the list of images
                self.recipes[self.currentImage].images.append(image)
        
        # Set the selected image into the last image in the list
        self.currentImage = (len(self.recipes[self.currentRecipe].images) - 1)
        # Refresh the displayed image
        self.refresh_image()

    def delete_image(self):
        """ Deletes the currently selected image """
        # TODO: Create a dialog that asks for confirmation from the user
        # Delete the image from the list of images
        deleted = (self.recipes[self.currentRecipe].
                images.pop(self.currentImage))
        # Check whether we are at the end of the images list
        if(self.currentImage == len(self.recipes[self.currentRecipe].images)):
            # Move back the currently selected image
            self.currentImage -= 1
        # Let's check if we still have any images, if not, use a placeholder
        if(len(self.recipes[self.currentRecipe].images) == 0):
            self.imageLabel.setPixmap(QPixmap("./gui/images/placeholder.png"))
            self.currentImage = 0
        else:
            # We still have an image, refresh the selected image
            self.refresh_image()

    def refresh_image(self):
        """
        Refreshes the image to the currently selected
        """
        self.imageLabel.setPixmap(self.recipes[self.currentRecipe].images[self.currentImage])

    def edit_ingredients(self):
        """
        Invokes the edit ingredients window, where the user can edit the
        ingredients of the currently selected recipe
        """
        # Create the dialog
        ingredientsDialog = IngredientsWindow(self,
                self.recipes[self.currentRecipe].ingredients)

        # Execute the dialog
        ingredientsDialog.exec_()

        # Get the updated list of ingredients from the dialog
        self.recipes[self.currentRecipe].ingredients = ingredientsDialog.get_ingredients()

        # Refresh the list of ingredients
        self.refresh_ingredients()

    def refresh_ingredients(self):
        """
        Refreshes the list of ingredients for the current selected recipe.
        """
        self.ingredientsData.clear() # clear the list first
        
        # Let's check first if the recipe has any ingredients.
        # If not, we will put a dummy entry in the ingredients so that the user
        # can add one.
        counter = 1 # Counter variable

        # Put the text in the ingredients list
        for ingredient in self.recipes[self.currentRecipe].ingredients:
            # Go through the list of ingredients
            self.ingredientsData.addItem(str(counter) + '. ' +
                    ingredient['name'] + ': ' + str(ingredient['quantity']) +
                    ' ' + ingredient['unit'] + '\n')
            counter += 1

        self.ingredientsData.addItem("+ Add an Ingredient")

    def refresh_instructions(self):
        """
        Refreshes the list of instructions for the current selected recipe.
        """
        self.instructionsData.clear() # clear the list
        
        # Let's check first if the recipe has any instructions.
        # If not, we will put a dummy entry in the instructions so that the
        # user can add one.
        counter = 1 # Counter variable
    
        # Put text in the instructions list
        for instruction in self.recipes[self.currentRecipe].instructions:
            # Go through the list of instructions
            self.instructionsData.addItem(str(counter) + '. ' +
                instruction + '\n')
            counter += 1

        self.instructionsData.addItem("+ Add an Instruction")

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

        # Clean the fields
        self.clear_data()

    def init_ui(self):
        """
        Function that initializes the UI components of the app.
        Only initialization is done here.
        """
        # Creation
        # Creates UI components, but does not link them together yet.
        
        self.mainLayout = QVBoxLayout() # main layout
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
        # Actions for menu and possibly one of the toolbars
        self.newRecipeAct = QAction(QIcon().fromTheme("document-new"), 
                "New Recipe...", self)
        self.importRecipeAct = QAction(QIcon().fromTheme("document-open"), 
                "Import Recipe...", self)
        self.exportRecipeAct = QAction(QIcon().fromTheme("document-save-as"), 
                "Export Recipe...", self)
        self.deleteRecipeAct = QAction(QIcon().fromTheme("edit-delete"), 
                "Delete Recipe...", self)
        self.quitAct = QAction(QIcon().fromTheme("application-exit"),
                "Quit...", self)
        # Keybinds for the different actions
        # These are platform dependent!
        self.newRecipeAct.setShortcuts(QKeySequence.New)
        self.importRecipeAct.setShortcuts(QKeySequence.Open)
        self.exportRecipeAct.setShortcuts(QKeySequence.SaveAs)
        self.deleteRecipeAct.setShortcuts(QKeySequence.Delete)
        self.quitAct.setShortcuts(QKeySequence.Quit)
        # Connect the actions to their respective slots
        self.connect(self.newRecipeAct, SIGNAL("triggered()"), self,
                SLOT("add_recipe()"))
        self.connect(self.importRecipeAct, SIGNAL("triggered()"), self,
                SLOT("import_recipe()"))
        self.connect(self.exportRecipeAct, SIGNAL("triggered()"), self,
                SLOT("export_recipe()"))
        self.connect(self.deleteRecipeAct, SIGNAL("triggered()"), self,
                SLOT("delete_recipe()"))
        self.connect(self.quitAct, SIGNAL("triggered()"), self,
                SLOT("close()"))

        self.fileMenu.addAction(self.newRecipeAct)
        self.fileMenu.addAction(self.importRecipeAct)
        self.fileMenu.addAction(self.exportRecipeAct)
        self.fileMenu.addAction(self.deleteRecipeAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Generate Shopping List")
        self.fileMenu.addAction(self.quitAct)
        self.editMenu.addAction("Ingredients")
        self.editMenu.addAction("Instructions")
        self.editMenu.addAction("Images")
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

        # The toolbar for the shinylist
        self.listTools = QToolBar()
        self.listTools.addAction(self.newRecipeAct)
        self.listTools.addAction(self.importRecipeAct)
        self.listTools.addAction(self.exportRecipeAct)
        self.listTools.addAction(self.deleteRecipeAct)

        ######################################################################
        # Recipe overview items
        ######################################################################
        # Layouts
        self.recipeOverviewGroup = QGroupBox("Recipe Details")
        self.recipeOverviewLayout = QGridLayout()
        
        # Items and labels
        self.nameData = QLineEdit(self)
        self.courseData = QComboBox()
        self.courseData.insertItem(0, "Appetizer")
        self.courseData.insertItem(1, "Main")
        self.courseData.insertItem(2, "Dessert")
        self.servingSizeData = QDoubleSpinBox(self)
        self.ingredientsData = QListWidget()
        self.instructionsData = QListWidget()
        # Set wrapping for the instructions and ingredients
        self.ingredientsData.setWordWrap(True)
        self.instructionsData.setWordWrap(True)

        ######################################################################
        # Generate shopping list items
        ######################################################################
        self.shoppingImagesLayout = QVBoxLayout()
        self.shoppingListLayout = QGridLayout()
        self.shoppingListGroup = QGroupBox("Generate Shopping List")

        self.generateServingSize = QDoubleSpinBox()
        self.generatedList = QTextBrowser()

        self.shoppingListGroup.setLayout(self.shoppingListLayout)
        generateInstructions = QLabel("Automatically calculate the amount " +
                "of ingredients needed given the serving size provided.")
        generateInstructions.setWordWrap(True)
        self.shoppingListLayout.addWidget(generateInstructions, 0, 1)
        self.shoppingListLayout.addWidget(QLabel("Serving Size"), 1, 0)
        self.shoppingListLayout.addWidget(self.generateServingSize, 1, 1)
        self.shoppingListLayout.addWidget(QLabel("You will need"), 2, 0)
        self.shoppingListLayout.addWidget(self.generatedList)

        ######################################################################
        # Images items
        ######################################################################
        self.imageLayout = QVBoxLayout()
        self.imageGroup = QGroupBox("Images")
        self.imageTools = QToolBar()

        # Image manipulation actions
        self.nextImageAct = QAction(QIcon().fromTheme("go-next"),
                "Next Image", self)
        self.prevImageAct = QAction(QIcon().fromTheme("go-previous"),
                "Preview Image", self)
        self.newImageAct = QAction(QIcon().fromTheme("list-add"), "New Image",
                self)
        self.deleteImageAct = QAction(QIcon().fromTheme("edit-delete"),
                "Remove Image", self)

        # Signals and slots for these image actions
        self.connect(self.nextImageAct, SIGNAL("triggered()"), self,
                SLOT("self.next_image()"))
        self.connect(self.prevImageAct, SIGNAL("triggered()"), self,
                SLOT("self.previous_image()"))
        self.connect(self.newImageAct, SIGNAL("triggered()"), self,
                SLOT("self.import_image()"))
        self.connect(self.deleteImageAct, SIGNAL("triggered()"), self,
                SLOT("self.delete_image()"))

        # Add the actions into the toolbar
        self.imageTools.addAction(self.prevImageAct)
        self.imageTools.addAction(self.newImageAct)
        self.imageTools.addAction(self.deleteImageAct)
        self.imageTools.addAction(self.nextImageAct)

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap("./gui/images/placeholder.png"))
        self.imageLabel.setScaledContents(True)

        self.imageLayout.addWidget(self.imageLabel)
        self.imageLayout.addWidget(self.imageTools)
        self.imageGroup.setLayout(self.imageLayout)
        
        # Layouting
        # Time to link together the different UI components
        self.setLayout(self.mainLayout) # set the main layout

        # Put the menubar in the main layout
        self.mainLayout.addWidget(self.menuBar)

        # Put the column layout in the main layout
        self.mainLayout.addLayout(self.columnLayout)

        # Put the list layout in the first slot of the column layout
        self.columnLayout.addLayout(self.listLayout)

        # Put the groupbox in the second column
        self.columnLayout.addWidget(self.recipeOverviewGroup)
        # Assign the layout to the group
        self.recipeOverviewGroup.setLayout(self.recipeOverviewLayout)

        # Put the right column items into the third column
        self.columnLayout.addLayout(self.shoppingImagesLayout)

        # Put the shopping list and images into their respective layouts
        self.shoppingImagesLayout.addWidget(self.shoppingListGroup)
        self.shoppingImagesLayout.addWidget(self.imageGroup)

        # Put the items and labels of a recipe into the recipe overview grid
        # layout
        self.recipeOverviewLayout.addWidget(QLabel("Recipe Name"),
                0, 0)
        self.recipeOverviewLayout.addWidget(self.nameData, 0, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Course"), 1, 0)
        self.recipeOverviewLayout.addWidget(self.courseData, 1, 1)
        self.recipeOverviewLayout.addWidget(QLabel("Serving Size"), 2, 0)
        self.recipeOverviewLayout.addWidget(self.servingSizeData, 2, 1)
        ingredientLabel = QLabel("Ingredients")
        ingredientLabel.setAlignment(Qt.AlignTop)
        self.recipeOverviewLayout.addWidget(ingredientLabel, 3, 0)
        self.recipeOverviewLayout.addWidget(self.ingredientsData, 3, 1)
        instructionLabel = QLabel("Instructions")
        instructionLabel.setAlignment(Qt.AlignTop)
        self.recipeOverviewLayout.addWidget(instructionLabel, 4, 0)
        self.recipeOverviewLayout.addWidget(self.instructionsData, 4, 1)

        # Put the shinylist in the list layout
        self.listLayout.addWidget(self.recipeList)
        # Put the shinylist tools in the list layout
        self.listLayout.addWidget(self.listTools)

        # Initialize the buttons signals and slots
        # Signal for when an item is clicked in the shinylist
        self.recipeList.clicked.connect(self.shinylist_click)
        # Signals for when an ingredient is double-clicked
        self.ingredientsData.doubleClicked.connect(self.edit_ingredients)
        # Signals for when an instruction is double-clicked
        self.instructionsData.doubleClicked.connect(self.edit_instructions)

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

        # Create list of recipes
        self.recipes = []
        # A variable to track the current recipe selected
        self.currentRecipe = 0
        # A variable that tracks the current image of the recipe selected
        self.currentImage = 0
        # Create a list of shinylist items
        self.shinyListItems = []
        self.init_ui() # Initialize the ui
