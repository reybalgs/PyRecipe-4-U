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

    def submit(self):
        print 'Form submitted!'
        self.done()

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


class EditRecipeWindow(RecipeWindow):
    """
    Window dialog that is called whenever we need to add a recipe into the
    system
    """
    def __init__(self, parent):
        super(EditRecipeWindow, self).__init__(parent)

        # Change some of the names of the elements
        self.windowTitle.setText("Edit Recipe")

        # Initialize the layout
        self.init_layout()
