###############################################################################
#
# ingredients.py
#
# This module contains the dialog that pops up whenever the user needs to view
# or edit ingredients.
#
###############################################################################

# Pyside imports
from PySide.QtCore import *
from PySide.QtGui import *

class IngredientEdit(QDialog):
    """
    A smaller dialog that contains the form data that allows the user to
    edit an ingredient's name, quantity, and unit.
    """
    def get_ingredient(self):
        """
        Returns the ingredient to the array of ingredients in the parent
        window
        """
        ingredient = [self.nameData.text(), self.quantityData.value(),
                      self.unitData.text()]

        return ingredient

    def submit(self):
        """
        Submits the data. Or rather, just closes the dialog in a neat fashion
        """
        self.done(1)

    def __init__(self, parent, ingredient = ()):
        """
        Initializes the window and its UI components.
        """
        super(IngredientEdit, self).__init__(parent)

        # Main Layout
        self.mainLayout = QVBoxLayout()
        # Form layout
        self.formLayout = QFormLayout()

        # Name input
        self.nameData = QLineEdit()
        # Quantity input
        self.quantityData = QDoubleSpinBox()
        # Unit input
        self.unitData = QLineEdit()

        # Save button
        self.saveButton = QPushButton("Save")

        # Initialize the signals of the button
        self.saveButton.clicked.connect(self.submit)

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.formLayout)
        self.formLayout.addRow("Name:", self.nameData)
        self.formLayout.addRow("Qty:", self.quantityData)
        self.formLayout.addRow("Unit:", self.unitData)
        self.mainLayout.addWidget(self.saveButton)


class IngredientsWindow(QDialog):
    """
    Window that gets invoked whenever the user needs to view or edit the
    ingredients of a recipe.
    """
    def get_ingredients(self):
        """
        Returns the array of ingredients.
        """
        return self.ingredients

    def initialize_list(self):
        """
        Initializes the listview of ingredients by referring to the list of
        ingredients inside the dialog.
        """
        # Clear the 
        for item in self.ingredients:
            self.ingredientsList.addItem(str(item[0]) + " - (" + str(item[1]) +
                                         " " + str(item[2]) + ")")

    def add_ingredient(self):
        """
        Creates a new ingredient by invoking an ingredient data dialog and
        getting its values.
        """
        ingredientEditDialog = IngredientEdit(self)
        ingredientEditDialog.exec_() # Execute the dialog
        ingredient = ingredientEditDialog.get_ingredient()
        self.ingredients.append(ingredientEditDialog.get_ingredient())
        self.ingredientsList.addItem(str(ingredient[0]) + " - (" +
                                     str(ingredient[1]) + " " +
                                     str(ingredient[2]) + ")")

    def __init__(self, parent, ingredients):
        """
        Initializes the window and its UI components, as well as the array
        of ingredients that it will pass back to its parent window.
        """
        super(IngredientsWindow, self).__init__(parent)

        # Main layout
        self.mainLayout = QVBoxLayout()
        # Signal for when an item is clicked in the shinylist

        self.headerLabel = QLabel("Ingredients")

        # The listwidget of ingredients
        self.ingredientsList = QListWidget()
        
        # A handy label with instructions
        self.helpLabel = QLabel("Click an ingredient on the list to edit it.\n"
                                + "Clicking Add Ingredient will add a new " +
                                " ingredient to the list.")

        # Add ingredient button
        self.addIngredientButton = QPushButton("Add Ingredient")

        # Edit ingredient button
        self.editIngredientButton = QPushButton("Edit Ingredient")

        # Delete ingredient button
        self.deleteIngredientButton = QPushButton("Delete Ingredient")

        # Save changes button
        self.saveChangesButton = QPushButton("Save Changes")

        # Time to arrange the UI elements into a layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.headerLabel)
        self.mainLayout.addWidget(self.ingredientsList)
        self.mainLayout.addWidget(self.helpLabel)
        self.mainLayout.addWidget(self.addIngredientButton)
        self.mainLayout.addWidget(self.editIngredientButton)
        self.mainLayout.addWidget(self.deleteIngredientButton)
        self.mainLayout.addWidget(self.saveChangesButton)

        # Initialize the button signals
        self.addIngredientButton.clicked.connect(self.add_ingredient)

        # Set the ingredients in this window to the one that was passed by
        # the parent window
        self.ingredients = ingredients
