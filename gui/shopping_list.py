##############################################################################
#
# shopping_list.py
#
# Python module that contains code necessary for the creation of the dialog
# that handles the application's "Generate Shopping List" functionality.
#
##############################################################################

# PySide imports
from PySide.QtCore import *
from PySide.QtGui import *

import sys

class ShoppingListDialog(QDialog):
    """
    Class of the dialog that pops up whenever the user wants to generate a
    shopping list for a specified ingredient.
    """
    def exit(self):
        """
        Exits the dialog graciously.
        """
        self.done(1)

    def refresh_data(self):
        """
        A function that catches the signal whenever the value in the new
        serving size double spinbox gets changed.
        """
        # Reinitialize the list
        self.initialize_list()

    def initialize_list(self):
        """
        Initializes the list of ingredients displayed in the list. The
        ingredients' values are based on the new values inputted by the user
        on the dialog's double spinbox.
        """
        # First we remove all the items in the list
        self.ingredientsList.clear()

        for ingredient in self.recipe.ingredients:
            # Loop for every ingredient in the list of ingredients of the
            # given recipe
            self.ingredientsList.addItem(str(ingredient[0]) + "- (" +
                str((ingredient[1] / self.recipe.servingSize) *
                self.newServingSizeData.value()) + " " +
                str(ingredient[2]) + ")")

    def init_signals(self):
        """
        Initializes the signals of the widgets that are supposed to give out
        signals.
        """
        self.exitButton.clicked.connect(self.exit)
        self.newServingSizeData.valueChanged.connect(self.refresh_data)

    def init_ui(self):
        """
        Initializes the ui components of the dialog and puts them around on
        layouts.
        """
        # Main layout
        self.mainLayout = QVBoxLayout()
        # Main text title
        self.mainTitle = QLabel("Generate Shopping List")
        # Form Layout
        self.formLayout = QFormLayout()

        # Original serving size data
        self.origServingSizeData = QLabel(str(self.recipe.servingSize))
        # New serving size data
        self.newServingSizeData = QDoubleSpinBox()
        # Set the data to the given recipe's
        self.newServingSizeData.setValue(self.recipe.servingSize)

        # List of ingredients
        self.ingredientsList = QListWidget()

        # Exit button
        self.exitButton = QPushButton("Return to Main Menu")

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.mainTitle)
        self.mainLayout.addLayout(self.formLayout)

        # For the form
        self.formLayout.addRow("Original Serving Size: ", 
                               self.origServingSizeData)
        self.formLayout.addRow("New Serving Size: ", self.newServingSizeData)

        self.mainLayout.addWidget(self.ingredientsList)
        
        # Refresh the list
        self.initialize_list()

        # Exit button
        self.mainLayout.addWidget(self.exitButton)

    def __init__(self, parent, recipe):
        """
        Initialization function. Mostly just calls an init ui function and
        a function that initializes the signals and slots
        """
        super(ShoppingListDialog, self).__init__(parent)
        # Put the given recipe in this dialog's own copy
        self.recipe = recipe

        self.init_ui()
        self.init_signals()
