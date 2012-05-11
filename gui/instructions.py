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

        Update: Now also affects the MoveUp and MoveDown buttons
        """
        self.editInstructionButton.setEnabled(True)
        self.deleteInstructionButton.setEnabled(True)
        self.moveUpButton.setEnabled(True)
        self.moveDownButton.setEnabled(True)

    def disable_buttons(self):
        """
        Disables the Edit, Delete, MoveUp and MoveDown buttons. Called whenever
        an item was just modified or moved in the list.
        """
        self.editInstructionButton.setEnabled(False)
        self.deleteInstructionButton.setEnabled(False)
        self.moveUpButton.setEnabled(False)
        self.moveDownButton.setEnabled(False)

    def move_instruction_up(self):
        """
        Moves an instruction up both lists of instructions. If the instruction
        is the first instruction in the list, do not do anything.
        """
        # Get the index of the currently selected instruction.
        index = self.instructionsList.currentRow()

        if index == 0:
            # Item selected is first, don't do anything
            print 'Item is already at top!'
        else:
            # Item can be moved up
            # Store the instruction in a temporary variable first
            instruction = self.instructions[index]
            # Pop the last location of the instruction
            self.instructions.pop(index)
            # Put the instruction behind the item that was last behind it
            self.instructions.insert(index - 1, instruction)
            # Move the current row to the instruction's new position
            self.instructionsList.setCurrentRow(index - 1)

            # Reinitialize the list
            self.initialize_list()

            # Disable the buttons
            self.disable_buttons()

    def move_instruction_down(self):
        """
        Moves an instruction down both lists of instructions. If the instruction
        is at the bottom of the list, do not do anything.
        """
        # Get the index of the currently selected instruction.
        index = self.instructionsList.currentRow()

        if index == len(self.instructions):
            # Item selected is the last, don't do anything
            print 'Item is already at bottom!'
        else:
            # Item can be moved down
            # Store the instruction in a temporary variable first
            instruction = self.instructions[index]
            # Pop the last location of the instructon
            self.instructions.pop(index)
            # Put the instruction after the item that was last in front of it
            self.instructions.insert(index + 1, instruction)
            # Move the current row to the instruction's new position
            self.instructionsList.setCurrentRow(index + 1)

            # Reinitialize the list
            self.initialize_list()

            # Disable the edit and delete buttons
            self.disable_buttons()

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
        self.disable_buttons()

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
        self.disable_buttons()

    def __init__(self, parent, instructions):
        """
        Initializes the window and its UI compoenents, as well as the array
        of instructions that it will pass back to its parent window.
        """
        super(InstructionsWindow, self).__init__(parent)

        # Main layout
        self.mainLayout = QVBoxLayout()
        # Split layout for move buttons and list
        self.splitLayout = QHBoxLayout()
        # Layout for move up/down buttons
        self.moveButtonLayout = QVBoxLayout()
        
        self.headerLabel = QLabel("Recipe Instructions")

        # The listwidget of instructions
        self.instructionsList = QListWidget()
        # Make the list word wrap enabled
        self.instructionsList.setWordWrap(True)

        # A handy label with helpful instructions
        self.helpLabel = QLabel("Click an Instruction above on the list to" +
                " edit it.\nClicking Add Instruction will add a new instruction"
                + " to the list.")

        # Move instruction buttons
        self.moveUpButton = QPushButton("MoveUp")
        self.moveDownButton = QPushButton("MoveDn")

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
        self.mainLayout.addLayout(self.splitLayout)
        self.splitLayout.addWidget(self.instructionsList)
        self.splitLayout.addLayout(self.moveButtonLayout)
        self.moveButtonLayout.addWidget(self.moveUpButton)
        self.moveButtonLayout.addWidget(self.moveDownButton)
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
        # Moving instructions in the list functions
        self.moveUpButton.clicked.connect(self.move_instruction_up)
        self.moveDownButton.clicked.connect(self.move_instruction_down)
        # Disable the edit and delete buttons first so that the user will be
        # encouraged to select an item first
        self.disable_buttons()
        # Connect list to a function that enables them
        self.instructionsList.itemClicked.connect(self.enable_buttons)

        # Initialize the list of instructions
        self.initialize_list()
