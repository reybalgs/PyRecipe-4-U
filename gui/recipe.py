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
    def init_signals(self):
        """Initializes the signals of the buttons in the dialog"""
        # TODO: Actually put something here

    def init_ui(self):
        """Initializes the UI of the dialog"""
        # Element creation
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        
        self.nameData = QLabel(self.recipe.name)
        self.courseData = QLabel(self.recipe.course)
        self.servingSizeData = QLabel(str(self.recipe.servingSize) + " people")

        self.ingredientData = QTextBrowser()
        self.instructionData = QTextBrowser()

        counter = 1 # A counter variable

        # Put text in the ingredients list
        for ingredient in self.recipe.ingredients:
            # Go through the list of ingredients
            self.ingredientData.insertPlainText(str(counter) + '. ' + 
                    ingredient[0] + ': ' + str(ingredient[1]) + ' ' +
                    ingredient[2] + '\n')
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

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.formLayout)

        self.formLayout.addRow("<b>Name:</b>", self.nameData)
        self.formLayout.addRow("<b>Course:</b>", self.courseData)
        self.formLayout.addRow("<b>Serving Size:</b>", self.servingSizeData)
        self.formLayout.addRow("<b>Ingredients:</b>", self.ingredientData)
        self.formLayout.addRow("<b>Instructions:</b>", self.instructionData)

    def __init__(self, parent, recipe):
        super(RecipeOverview, self).__init__(parent)
        self.recipe = recipe # Get the recipe passed
        self.setWindowTitle("Overview for " + self.recipe.name)

        self.init_ui()
        self.init_signals()

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
        self.ingredientsButton = QPushButton("Ingredients")
        self.instructionsButton = QPushButton("Instructions")
        self.submitButton = QPushButton("Submit")

        self.recipe = RecipeModel() # Create a model

    def edit_ingredients(self):
        """
        Invokes a window that handles all the operations on ingredients such
        as viewing and editing.
        """
        editIngredientsWindow = IngredientsWindow(self, 
                                                  self.recipe.ingredients)
        editIngredientsWindow.exec_() # Execute the dialog
        # Get the ingredients from the dialog
        self.recipe.ingredients = editIngredientsWindow.get_ingredients()

    def edit_instructions(self):
        """
        Invokes a window that handles all the operations on a recipe's list
        of instructions such as viewing and editing.
        """
        editInstructionsWindow = InstructionsWindow(self,
                                                    self.recipe.instructions)
        editInstructionsWindow.exec_() # Execute the dialog
        # Get the instructions from the dialog
        self.recipe.instructions = editInstructionsWindow.get_instructions()

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
        self.buttonLayout.addWidget(self.ingredientsButton)
        self.buttonLayout.addWidget(self.instructionsButton)

        # Add the submit button
        self.mainLayout.addWidget(self.submitButton)

        # Set the mainlayout as the layout of the entire window
        self.setLayout(self.mainLayout)

    def init_signals(self):
        """
        Initializes the signal of the submit button
        """
        self.submitButton.clicked.connect(self.submit)
        self.ingredientsButton.clicked.connect(self.edit_ingredients)
        self.instructionsButton.clicked.connect(self.edit_instructions)


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
