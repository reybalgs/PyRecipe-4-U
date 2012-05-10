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

import sys

class RecipeWindow(QDialog):
    """
    The main class of all the windows that deal with the manipulation of
    recipes.

    Does not have a __init__ method. Rather, the subclasses of this class
    are the ones that should be called.
    """
    def __init__(self, parent):
        super(RecipeWindow, self).__init__(parent)
        self.windowTitle = QLabel("Add/Edit Recipe")

        # Form stuff
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.buttonLayout = QHBoxLayout()
        # Name
        self.nameData = QLineEdit()
        # Course
        self.courseData = QComboBox()
        # Adding items to the course combobox
        self.courseData.addItem("Appetizer")
        self.courseData.addItem("Main")
        self.courseData.addItem("Dessert")
        # Serving Size
        self.servingSizeData = QDoubleSpinBox()

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
        # Put all the information in the forms into the model
        self.recipe.name = self.nameData.text()
        self.recipe.course = self.courseData.currentText()
        self.recipe.servingSize = self.servingSizeData.value()

        print 'Form submitted!'
        self.done(1)

    def init_layout(self):
        """
        Initializes the layout of the dialog. Usually called by its subclasses.
        """
        self.mainLayout.addWidget(self.windowTitle)
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


class AddRecipeWindow(RecipeWindow):
    """
    Window dialog that is called whenever we need to add a recipe into
    the system
    """
    def __init__(self, parent):
        super(AddRecipeWindow, self).__init__(parent)

        # Change some of the names of the elements
        self.windowTitle.setText("Add Recipe")

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
        self.windowTitle.setText("Edit Recipe")

        # Initialize the layout
        self.init_layout()
        # Initialize signals
        self.init_signals()

        # Initialize the recipe to be edited
        self.recipe = recipe

        # Refresh the data fields to reflect the current recipe data
        self.refresh_data()
