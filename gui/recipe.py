###############################################################################
#
# recipe.py
#
# This module contains all of the classes and functions that are shared by the
# Add Recipe and Edit Recipe dialogs.
#
# I chose to consolidate them into one module because they are quite similar in
# nature.
#
###############################################################################

# PySide imports
from PySide.QtCore import *
from PySide.QtGui import *

# Import recipe model
from models.recipemodel import *

# Ingredients window import
from ingredients import *

# Instructions window import
from instructions import *

# Error dialog import
from errordialog import *

import sys

class RecipeOverview(QDialog):
    """
    The class of the dialog that shows an overview of an entire recipe. Does
    not actually edit the recipe, but has buttons that lead to editing
    functionalities.
    """
    def get_recipe(self):
        """Returns the recipe inside this dialog"""
        return self.recipe

    def refresh_recipe_info(self):
        """
        Refreshes the essential data of the recipe in view, usually done after
        an edit.
        """
        self.nameData.setText(self.recipe.name)
        self.courseData.setText(self.recipe.course)
        self.servingSizeData.setText(str(self.recipe.servingSize) + ' people')

    def refresh_ingredients(self):
        """Refreshes the recipe's list of ingredients"""
        self.ingredientData.clear() # clear the list

        counter = 1 # A counter variable

        # Put text in the ingredients list
        for ingredient in self.recipe.ingredients:
            # Go through the list of ingredients
            self.ingredientData.insertPlainText(ingredient['name'] + ': ' + 
                    str(ingredient['quantity']) + ' ' + ingredient['unit'])
            counter += 1

    def refresh_instructions(self):
        """Refreshes the recipe's list of instructions"""
        self.instructionData.clear() # clear the llist

        counter = 1 # A counter variable

        for instruction in self.recipe.instructions:
            # Go through the list of instructions
            self.instructionData.insertPlainText(str(counter) + '. ' +
                    instruction + '\n')
            counter += 1


    def edit_recipe_info(self):
        """Edits the essential data of the recipe in view"""
        # Create an edit recipe dialog
        editRecipeDialog = EditRecipeWindow(self, self.recipe)

        # Execute the dialog
        editRecipeDialog.exec_()

        # Return the recipe from the dialog
        self.recipe = editRecipeDialog.get_recipe()

        # Refresh the info displayed
        self.refresh_recipe_info()
        
    def edit_ingredients(self):
        """Edits the ingredients of the recipe in view"""
        # Create an ingredients dialog
        ingredientsDialog = IngredientsWindow(self, self.recipe.ingredients)

        # Execute the dialog
        ingredientsDialog.exec_()

        # Get the updated list of ingredients from the dialog
        self.recipe.ingredients = ingredientsDialog.get_ingredients()

        # Refresh the list of ingredients
        self.refresh_ingredients()

    def edit_instructions(self):
        """Edits the instructions of the recipe in view"""
        # Create an instructions dialog
        instructionsDialog = InstructionsWindow(self,
                self.recipe.instructions)

        # Execute the dialog
        instructionsDialog.exec_()

        # Get the updated list of instructions from the dialog
        self.recipe.instructions = instructionsDialog.get_instructions()

        # Refresh the list of instructions
        self.refresh_instructions()

    def import_image(self):
        """Imports an image to be used by the current recipe"""
        # Create a var containing a list of images
        files = ''
        # Create a var that contains the path of the actual image
        path = ''
        # Invoke a filedialog that will look for the image
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        #fileDialog.setNameFilter("Image Files(*.png, *.jpg, *.jpeg, *.gif" +
        #        ", *.bmp")

        if fileDialog.exec_():
            files = fileDialog.selectedFiles()
            path = files[0]
            print path + ' loaded!'

        if (path) and (path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif',
                '.bmp'))):
            # There is an image
            # Put the image path into the list of images on this recipe.
            self.recipe.images.append(path)
            print self.recipe.name + ' images: ' + str(self.recipe.images)

        # Now we have to set the image of the dish to the newly-imported image.
        self.selectedImage = (len(self.recipe.images) - 1)
        # Set the displayed image to the selected image
        self.imageLabel.setPixmap(QPixmap(path).scaledToWidth(420))
        # Refresh the image buttons
        self.toggle_image_buttons()
        print self.selectedImage

    def delete_image(self):
        """Deletes the currently selected image"""
        # TODO: Create a dialog that warns the user when there is only one
        # image in the recipe
        # Delete the image from the list of images
        deleted = self.recipe.images.pop(self.selectedImage)
        if(self.selectedImage == len(self.recipe.images)):
            # We are at the end of the list
            self.selectedImage -= 1
        if(len(self.recipe.images) == 0):
            # We don't have any images anymore
            self.imageLabel.setPixmap(QPixmap("./gui/images/placeholder.png"))
            self.selectedImage = 0
        else:
            # We still have an image
            self.imageLabel.setPixmap(QPixmap(
                self.recipe.images[self.selectedImage]).scaledToWidth(420))
        # Refresh the buttons
        self.toggle_image_buttons()
        print str(deleted) + ' has been removed from the list of images!'

    def next_image(self):
        """
        Changes the currently displayed image to the next image in the recipe's
        sequence of images, if any.
        """
        if len(self.recipe.images) > 1:
            # We have an image to go to
            if self.selectedImage < (len(self.recipe.images) - 1):
                # We are not at the end of of the image list, we can move
                # forward
                # Increment the selected image index
                self.selectedImage += 1
                # Change the displayed image
                self.imageLabel.setPixmap(QPixmap(
                    self.recipe.images[self.selectedImage]).scaledToWidth(420))
                # Toggle the buttons
                self.toggle_image_buttons()
            else:
                print 'Already at the end of the image list!'

    def previous_image(self):
        """
        Changes the curently displayed image to the previous image in the
        recipe's sequence of images, if any.
        """
        if len(self.recipe.images) > 1:
            # We have an image to go to
            if self.selectedImage > 0:
                # We are not at the beginning so we can move back once
                # Decrement the selected image index
                self.selectedImage -= 1
                # Change the displayed image
                self.imageLabel.setPixmap(QPixmap(
                    self.recipe.images[self.selectedImage]).scaledToWidth(420))
                # Toggle the buttons
                self.toggle_image_buttons()
            else:
                print 'Already at the beginning of the list!'

    def toggle_image_buttons(self):
        """
        Disables and/or enables the some of the image buttons depending on the 
        current state of the recipe.
        """
        if (len(self.recipe.images) < 2):
            # We have only one or no image for this recipe
            # Disable the previous and next image buttons
            self.prevImageButton.setEnabled(False)
            self.nextImageButton.setEnabled(False)
            if (len(self.recipe.images) == 0):
                # We have no images, so disable the delete button as it makes
                # no sense.
                self.deleteImageButton.setEnabled(False)
            else:
                # There's at least one image, allow the user to delete that
                # recipe
                self.deleteImageButton.setEnabled(True)
        else:
            # There are two or more recipes
            # We have to disable and enable the buttons based on the current
            # image selected for the recipe.
            # 
            # First let's enable the delete image button
            self.deleteImageButton.setEnabled(True)
            if self.selectedImage == 0:
                # We are at the first image, disable the prev image button
                self.prevImageButton.setEnabled(False)
                self.nextImageButton.setEnabled(True)
            elif self.selectedImage == ((len(self.recipe.images)) - 1):
                # We are at the last image, disable the next image button
                self.prevImageButton.setEnabled(True)
                self.nextImageButton.setEnabled(False)
            else:
                # We are somewhere in the middle, enable both buttons
                self.prevImageButton.setEnabled(True)
                self.nextImageButton.setEnabled(True)

    def init_signals(self):
        """Initializes the signals of the buttons in the dialog"""
        # Buttons on the left side
        self.editRecipeButton.clicked.connect(self.edit_recipe_info)
        self.editIngredientsButton.clicked.connect(self.edit_ingredients)
        self.editInstructionsButton.clicked.connect(self.edit_instructions)
        self.newImageButton.clicked.connect(self.import_image)
        self.prevImageButton.clicked.connect(self.previous_image)
        self.nextImageButton.clicked.connect(self.next_image)
        self.deleteImageButton.clicked.connect(self.delete_image)

    def init_ui(self):
        """Initializes the UI of the dialog"""
        # Element creation
        self.mainLayout = QVBoxLayout()
        self.splitLayout = QHBoxLayout()
        self.formLayout = QFormLayout() # Layout for the left side
        self.rightHandLayout = QVBoxLayout() # Layout for the right side
        
        self.nameData = QLabel(self.recipe.name)
        self.courseData = QLabel(self.recipe.course)
        self.servingSizeData = QLabel(str(self.recipe.servingSize) + " people")
        
        # Button to edit the recipe's essential information
        self.editRecipeButton = QPushButton("Edit Recipe Information")
        self.editRecipeButton.setToolTip("Edit this recipe's vital " +
                "information (name, course, serving size)")

        self.ingredientData = QTextBrowser()
        self.editIngredientsButton = QPushButton("Edit Ingredients")
        self.editIngredientsButton.setToolTip("Edit the ingredients for " +
                "this recipe.")

        self.instructionData = QTextBrowser()
        self.instructionData.setMinimumWidth(360)
        self.editInstructionsButton = QPushButton("Edit Instructions")
        self.editInstructionsButton.setToolTip("Edit the instructions for " +
                "this recipe.")

        counter = 1 # A counter variable

        # Put text in the ingredients list
        for ingredient in self.recipe.ingredients:
            # Go through the list of ingredients
            self.ingredientData.insertPlainText(str(counter) + '. ' + 
                    ingredient['name'] + ': ' + str(ingredient['quantity']) + 
                    ' ' + ingredient['unit'] + '\n')
            counter += 1

        counter = 1
        # Put text in the instructions list
        for instruction in self.recipe.instructions:
            # Go through the list of instructions
            self.instructionData.insertPlainText(str(counter) + '. ' +
                    instruction + '\n')
            counter += 1

        self.buttonLayout = QHBoxLayout()
        self.editRecipeButton = QPushButton("Edit Recipe")
        self.editIngredientsButton = QPushButton("Edit Ingredients")
        self.editInstructionsButton = QPushButton("Edit Instructions")

        # Right hand side items
        # The recipe image
        self.imageLabel = QLabel("No image available")
        self.imageLabel.setPixmap(QPixmap("./gui/images/placeholder.png"))
        # Image chooser buttons
        # Layout for the buttons
        self.imageButtonsLayout = QHBoxLayout()
        self.prevImageButton = QPushButton("Previous")
        self.nextImageButton = QPushButton("Next")
        self.newImageButton = QPushButton("New Image")
        self.deleteImageButton = QPushButton("Delete Image")

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.splitLayout)
        self.splitLayout.addLayout(self.formLayout)
        self.splitLayout.addLayout(self.rightHandLayout)

        # Left hand side
        self.formLayout.addRow("<b>Name:</b>", self.nameData)
        self.formLayout.addRow("<b>Course:</b>", self.courseData)
        self.formLayout.addRow("<b>Serving Size:</b>", self.servingSizeData)
        self.formLayout.addRow("", self.editRecipeButton)
        self.formLayout.addRow("<b>Ingredients:</b>", self.ingredientData)
        self.formLayout.addRow("", self.editIngredientsButton)
        self.formLayout.addRow("<b>Instructions:</b>", self.instructionData)
        self.formLayout.addRow("", self.editInstructionsButton)

        # Right hand side
        self.rightHandLayout.addWidget(self.imageLabel)
        self.rightHandLayout.addLayout(self.imageButtonsLayout)
        self.imageButtonsLayout.addWidget(self.prevImageButton)
        self.imageButtonsLayout.addWidget(self.newImageButton)
        self.imageButtonsLayout.addWidget(self.deleteImageButton)
        self.imageButtonsLayout.addWidget(self.nextImageButton)

        # Toggling the image buttons
        self.toggle_image_buttons()

    def __init__(self, parent, recipe):
        super(RecipeOverview, self).__init__(parent)
        self.recipe = recipe # Get the recipe passed
        self.setWindowTitle("Overview for " + self.recipe.name)

        self.init_ui()
        self.init_signals()

        # A counter variable that keeps track of the currently selected
        # image for the recipe
        # Initialized at 0 because we always start from the start.
        self.selectedImage = 0

class RecipeWindow(QDialog):
    """
    The main class of all the windows that deal with the manipulation of
    recipes.

    Does not have a __init__ method. Rather, the subclasses of this class
    are the ones that should be called.
    """
    def __init__(self, parent):
        super(RecipeWindow, self).__init__(parent)
        
        # Form stuff
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.buttonLayout = QHBoxLayout()
        # Name
        self.nameData = QLineEdit()
        # Tooltip for the name data
        self.nameData.setToolTip("The name of your recipe.")
        # Course
        self.courseData = QComboBox()
        # Tooltip for the course data
        self.courseData.setToolTip("The course of your recipe.")
        # Adding items to the course combobox
        self.courseData.addItem("Appetizer")
        self.courseData.addItem("Main")
        self.courseData.addItem("Dessert")
        # Serving Size
        self.servingSizeData = QDoubleSpinBox()
        # Tooltip for the serving size data
        self.servingSizeData.setToolTip("How many people your recipe can " +
                "serve")

        # Buttons
        self.submitButton = QPushButton("Submit")

        self.recipe = RecipeModel() # Create a model

    def get_recipe(self):
        """
        Returns the recipe in this dialog
        """
        return self.recipe

    def submit(self):
        """
        Puts all the form data into a model and returns that model to the
        main screen
        """
        self.recipe.name = self.nameData.text()
        self.recipe.course = self.courseData.currentText()
        self.recipe.servingSize = self.servingSizeData.value()

        if not (self.recipe.name == '' or self.recipe.servingSize == 0.0):
            # Everything seems to be in order, so carry on
            # Put all the information in the forms into the model
            print 'Form submitted!'
            self.done(1)
        else:
            # Something is missing, raise the error dialog
            errorDialog = ErrorDialog(self, 'recipe')
            errorDialog.exec_() # execute the dialog
            if (errorDialog.get_flag() == 1):
                # User wanted to just discard the recipe
                self.done(1)

    def init_layout(self):
        """
        Initializes the layout of the dialog. Usually called by its subclasses.
        """
        self.mainLayout.addLayout(self.formLayout)

        # Initialize the form
        self.formLayout.addRow("Name:", self.nameData)
        self.formLayout.addRow("Course:", self.courseData)
        self.formLayout.addRow("Serving Size:", self.servingSizeData)

        # Add the instructions and ingredients buttons
        self.mainLayout.addLayout(self.buttonLayout)

        # Add the submit button
        self.mainLayout.addWidget(self.submitButton)

        # Set the mainlayout as the layout of the entire window
        self.setLayout(self.mainLayout)

    def init_signals(self):
        """
        Initializes the signal of the submit button
        """
        self.submitButton.clicked.connect(self.submit)

class AddRecipeWindow(RecipeWindow):
    """
    Window dialog that is called whenever we need to add a recipe into
    the system
    """
    def __init__(self, parent):
        super(AddRecipeWindow, self).__init__(parent)

        # Change some of the names of the elements
        self.setWindowTitle("Add Recipe")

        # Initialize the layout
        self.init_layout()
        # Initialize signals
        self.init_signals()


class EditRecipeWindow(RecipeWindow):
    """
    Window dialog that is called whenever we need to add a recipe into the
    system
    """
    def refresh_data(self):
        """
        Refreshes the data on the data fields. Ideally used at startup or
        whenever changes were made
        """
        # Set the name data
        self.nameData.setText(self.recipe.name)
        
        # Set the course data depending on the course given
        if self.recipe.course == 'Appetizer':
            self.courseData.setCurrentIndex(0)
        elif self.recipe.course == 'Main':
            self.courseData.setCurrentIndex(1)
        elif self.recipe.course == 'Dessert':
            self.courseData.setCurrentIndex(2)
        else:
            print 'Error! Wrong index/name of course!'

        # Set the recipe's serving size data
        self.servingSizeData.setValue(self.recipe.servingSize)

        # Some debug messages
        print 'Window refreshed!'



    def __init__(self, parent, recipe):
        super(EditRecipeWindow, self).__init__(parent)

        # Change some of the names of the elements
        self.setWindowTitle("Edit " + recipe.name)

        # Initialize the layout
        self.init_layout()
        # Initialize signals
        self.init_signals()

        # Initialize the recipe to be edited
        self.recipe = recipe

        # Refresh the data fields to reflect the current recipe data
        self.refresh_data()
