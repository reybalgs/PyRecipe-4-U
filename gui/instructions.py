##############################################################################
#
# instructions.py
#
# This module contains the dialogs that pop up whenever the user needs to
# manipulate the instructions of a recipe.
#
##############################################################################

# PySide imports
from PySide.QtCore import *
from PySide.QtGui import *

import sys

class InstructionEdit(QDialog):
    """
    A smaller variant of the instructions dialog whose sole purpose is to wait
    for user input for instructions.
    """
    def get_instruction(self):
        """
        Returns the instruction to the array of instructions in the parent
        window
        """
        # Get the value from the text edit
        self.instruction = self.instructionData.toPlainText()
        # Return the instruction
        return self.instruction

    def submit(self):
        """
        Exits the dialog in a neat fashion.
        """
        self.done(1)

    def __init__(self, parent, instruction = []):
        """
        Initializes the window and its UI components, as well as initialize
        the instruction that it will be manipulating.
        """
        super(InstructionEdit, self).__init__(parent)

        # the instruction to be edited
        self.instruction = instruction

        # If instruction is empty, this is probably a new instruction, so create
        # a dummy value
        if len(self.instruction) == 0:
            self.instruction = ''

        # Main layout
        self.mainLayout = QVBoxLayout()
        
        # Edit box
        self.instructionData = QTextEdit()
        self.instructionData.setText(self.instruction)

        # Save button
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.submit)

        # Layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.instructionData)
        self.mainLayout.addWidget(self.saveButton)

class InstructionsWindow(QDialog):
    def get_instructions(self):
        """
        Returns the list of instructions inside this dialog.
        """
        return self.instructions

    def submit(self):
        """
        Closes the dialog graciously.
        """
        self.done(1)

    def enable_buttons(self):
        """
        Enables the Edit and Delete instruction buttons. Called whenever an
        item is selected in the visible instructions list.
        """
        self.editInstructionButton.setEnabled(True)
        self.deleteInstructionButton.setEnabled(True)

    def initialize_list(self):
        """
        Initializes the listview of instructions by deleting everything then
        putting everything back together based on the list of instructions
        inside this dialog.
        """
        # Clear entire list
        self.instructionsList.clear()
        # Create a counter variable
        counter = 1
        # Put everything into the list
        for instruction in self.instructions:
            self.instructionsList.addItem(str(counter) + '. ' + instruction)
            counter += 1 # increment counter

    def add_instruction(self):
        """
        Creates a new instruction by invoking an instruction data dialog and
        getting the values from there.
        """
        instructionEditDialog = InstructionEdit(self)
        instructionEditDialog.exec_() # execute the dialog
        instruction = instructionEditDialog.get_instruction()
        # Add the instruction to the list of instructions
        self.instructions.append(instruction)
        # Refresh the list
        self.initialize_list()

    def edit_instruction(self):
        """
        Edits the currently selected instruction from the visible list of
        instructions.
        """
        # Get the index of the instruction selected
        index = self.instructionsList.currentRow()

        # Pass the selected instruction to an editing dialog
        instructionEditDialog = InstructionEdit(self, self.instructions[index])
        instructionEditDialog.exec_() # execute the dialog
        # Retreive the edited instruction from the dialog
        self.instructions[index] = instructionEditDialog.get_instruction()

        # Reinitialize the list
        self.initialize_list()

        # Disable the edit and delete instruction buttons
        self.editInstructionButton.setEnabled(False)
        self.deleteInstructionButton.setEnabled(False)

    def delete_instruction(self):
        """
        Deletes a selected instruction from both the list of instructions for
        the recipe nad the visible list of instructions.
        """
        # Get the index of the currently selected instruction.
        index = self.instructionsList.currentRow()

        # Remove the instruction from the list of instructions
        self.instructions.pop(index)
        # Refresh the visible list of instructions
        self.initialize_list()

        # Disable the edit and delete buttons again
        self.editInstructionButton.setEnabled(False)
        self.deleteInstructionButton.setEnabled(False)

    def __init__(self, parent, instructions):
        """
        Initializes the window and its UI compoenents, as well as the array
        of instructions that it will pass back to its parent window.
        """
        super(InstructionsWindow, self).__init__(parent)

        # Main layout
        self.mainLayout = QVBoxLayout()
        
        self.headerLabel = QLabel("Recipe Instructions")

        # The listwidget of instructions
        self.instructionsList = QListWidget()

        # A handy label with helpful instructions
        self.helpLabel = QLabel("Click an Instruction above on the list to" +
                " edit it.\nClicking Add Instruction will add a new instruction"
                + " to the list.")

        # Add Instruction button
        self.addInstructionButton = QPushButton("Add Instruction")

        # Edit Instruction button
        self.editInstructionButton = QPushButton("Edit Instruction")

        # Delete Instruction button
        self.deleteInstructionButton = QPushButton("Delete Instruction")

        # Save Changes button
        self.saveChangesButton = QPushButton("Save Changes")

        # Arrange the UI elements into a layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.headerLabel)
        self.mainLayout.addWidget(self.instructionsList)
        self.mainLayout.addWidget(self.helpLabel)
        self.mainLayout.addWidget(self.addInstructionButton)
        self.mainLayout.addWidget(self.editInstructionButton)
        self.mainLayout.addWidget(self.deleteInstructionButton)
        self.mainLayout.addWidget(self.saveChangesButton)
        
        # Set the instructions list in this window to the one that was passed
        # by the parent window
        self.instructions = instructions

        # Connect the signals to appropriate functions
        self.addInstructionButton.clicked.connect(self.add_instruction)
        self.saveChangesButton.clicked.connect(self.submit)
        # Edit functions
        self.instructionsList.doubleClicked.connect(self.edit_instruction)
        self.editInstructionButton.clicked.connect(self.edit_instruction)
        # Delete functions
        self.deleteInstructionButton.clicked.connect(self.delete_instruction)
        # Disable the edit and delete buttons first so that the user will be
        # encouraged to select an item first
        self.editInstructionButton.setEnabled(False)
        self.deleteInstructionButton.setEnabled(False)
        # Connect list to a function that enables them
        self.instructionsList.itemClicked.connect(self.enable_buttons)

        # Initialize the list of instructions
        self.initialize_list()