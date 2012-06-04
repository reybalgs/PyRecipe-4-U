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

# Import the error dialog
from errordialog import *

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
        self.ingredient['name'] = self.nameData.text()
        self.ingredient['quantity'] = self.quantityData.value()
        self.ingredient['unit'] = self.unitData.text()

        return self.ingredient

    def submit(self):
        """
        Submits the data. Or rather, just closes the dialog in a neat fashion
        """
        if not (self.nameData.text() == '' or self.quantityData.value() == 0.0
            or self.unitData.text() == ''):
                # No missing data, so carry on
                self.done(1)
        else:
            # There are missing data, invoke the error dialog
            errorDialog = ErrorDialog(self, 'ingredient')
            errorDialog.exec_()
            if (errorDialog.get_flag()):
                # The user wants to discard
                self.done(1)

    def refresh_data(self):
        """
        Refreshes the fields using the passed ingredient.
        """
        self.nameData.setText(self.ingredient['name'])
        self.quantityData.setValue(self.ingredient['quantity'])
        self.unitData.setText(self.ingredient['unit'])

    def __init__(self, parent, ingredient = {}):
        """
        Initializes the window and its UI components.
        """
        super(IngredientEdit, self).__init__(parent)

        # initialize the ingredient to be edited
        self.ingredient = ingredient

        # If the list is empty (len 0), then this is a new ingredient, create
        # some dummy values
        if len(self.ingredient) == 0:
            self.ingredient = {'name': '', 'quantity': 0.0, 'unit': ''}

        # Set the window title
        self.setWindowTitle("Add/Edit Ingredient")

        # Main Layout
        self.mainLayout = QVBoxLayout()
        # Form layout
        self.formLayout = QFormLayout()

        # Name input
        self.nameData = QLineEdit()
        self.nameData.setToolTip("The name of this ingredient")
        # Quantity input
        self.quantityData = QDoubleSpinBox()
        self.quantityData.setToolTip("How much of this ingredient is " +
                "needed (in its expressed units)")
        # Unit input
        self.unitData = QLineEdit()
        self.unitData.setToolTip("The unit of measurement for this " +
                "ingredient")

        # Save button
        self.saveButton = QPushButton("Save")
        self.saveButton.setToolTip("Saves the changes you made for this " +
                "ingredient")

        # Initialize the signals of the button
        self.saveButton.clicked.connect(self.submit)

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.formLayout)
        self.formLayout.addRow("Name:", self.nameData)
        self.formLayout.addRow("Qty:", self.quantityData)
        self.formLayout.addRow("Unit:", self.unitData)
        self.mainLayout.addWidget(self.saveButton)

        # Refresh the fields, in case we're editing or something
        self.refresh_data()

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

    def enable_buttons(self):
        """
        Enables the Edit and Delete ingredient buttons once the user has
        selected an item in the visible list.
        """
        self.deleteIngredientButton.setEnabled(True)

    def initialize_list(self):
        """
        Initializes the listview of ingredients by referring to the list of
        ingredients inside the dialog.
        """
        # Clear the list
        self.ingredientsList.clear()

        for ingredient in self.ingredients:
            self.ingredientsList.addItem(ingredient['name'] + ': ' + 
                    str(ingredient['quantity']) + ' ' +  ingredient['unit'])

    def add_ingredient(self):
        """
        Creates a new ingredient by invoking an ingredient data dialog and
        getting its values.
        """
        ingredientEditDialog = IngredientEdit(self)
        ingredientEditDialog.exec_() # Execute the dialog
        ingredient = ingredientEditDialog.get_ingredient()
        if not (ingredient['name'] == '' or ingredient['quantity'] == 0.0 or
                ingredient['unit'] == ''):
                    self.ingredients.append(ingredient)
                    self.initialize_list()

    def edit_ingredient(self):
        """
        Edits the currently selected ingredient from the visible list of
        ingredients.
        """
        # Get the index of the ingredient selected
        index = self.ingredientsList.currentRow()

        # Create an editing dialog and pass the selected ingredient to it
        ingredientEditDialog = IngredientEdit(self, self.ingredients[index])
        ingredientEditDialog.exec_() # execute the dialog
        # Retreive the edited ingredient from the dialog
        self.ingredients[index] = ingredientEditDialog.get_ingredient()

        # Reinitialize the list
        self.initialize_list()

        # Disable the edit and delete ingredient buttons again to "fool" the
        # user that their selection was reset
        self.deleteIngredientButton.setEnabled(False)

    def delete_ingredient(self):
        """
        Deletes an ingredient both from the list of ingredients and the visible
        list of ingredients.
        """
        # Get the index of the selected ingredient
        index = self.ingredientsList.currentRow()

        # Remove the ingredient from the list of ingredients
        self.ingredients.pop(index)
        # Refresh the visible list of ingredients
        self.initialize_list()

        # Disable the edit and delete ingredient buttons again to "fool" the
        # user that their selection was reset
        self.deleteIngredientButton.setEnabled(False)

    def submit(self):
        """
        Closes the dialog graciously.
        """
        self.done(1)        

    def __init__(self, parent, ingredients):
        """
        Initializes the window and its UI components, as well as the array
        of ingredients that it will pass back to its parent window.
        """
        super(IngredientsWindow, self).__init__(parent)
        self.setWindowTitle("Ingredients")

        # Main layout
        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        # The listwidget of ingredients
        self.ingredientsList = QListWidget()
        self.ingredientsList.setToolTip("Double click on an ingredient " +
                "to edit it.")
        
        # Add ingredient button
        self.addIngredientButton = QPushButton("Add")
        self.addIngredientButton.setToolTip("Add an ingredient for this " +
                "recipe")

        # Delete ingredient button
        self.deleteIngredientButton = QPushButton("Delete")
        self.deleteIngredientButton.setToolTip("Delete the selected " +
                "ingredient")
        # Give it properties similar to the edit ingredient button
        self.deleteIngredientButton.setEnabled(False)

        # Save changes button
        self.saveChangesButton = QPushButton("Save Changes")
        self.saveChangesButton.setToolTip("Saves all changes made and " +
                "returns to the recipe overview (close this window to " +
                "just discard your changes)")

        # Time to arrange the UI elements into a layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.ingredientsList)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.addIngredientButton)
        self.buttonLayout.addWidget(self.deleteIngredientButton)
        self.mainLayout.addWidget(self.saveChangesButton)

        # Initialize the button signals
        self.addIngredientButton.clicked.connect(self.add_ingredient)
        self.saveChangesButton.clicked.connect(self.submit)
        # For editing ingredients
        self.ingredientsList.doubleClicked.connect(self.edit_ingredient)
        # For deleting ingredients
        self.deleteIngredientButton.clicked.connect(self.delete_ingredient)
        # Enable the edit and delete ingredient buttons once an item has been
        # clicked or selected in the visible list
        self.ingredientsList.itemClicked.connect(self.enable_buttons)

        # Set the ingredients in this window to the one that was passed by
        # the parent window
        self.ingredients = ingredients

        # Initialize the list
        self.initialize_list()
