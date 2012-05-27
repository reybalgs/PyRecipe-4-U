###############################################################################
#
# errordialog.py
#
# The Python module that contains the code for the error dialog class shared
# by the recipe, ingredient and instruction edit dialogs. It is made to show
# up whenever the user has some missing information in their forms.
#
###############################################################################

# PySide imports
from PySide.QtCore import *
from PySide.QtGui import *

class ErrorDialog(QDialog):
    """
    The class of the dialog that pops up whenever the user has some missing
    information in whatever they're adding into the system.

    This does not pop up whenever the user just tries to close the dialog they
    are editing the recipe/instruction/ingredient from.
    """
    def get_flag(self):
        """Returns whether the user wanted to go back to edit or to discard."""
        return self.discard

    def discard_item(self):
        """
        Discards whatever the user was doing by raising the discard flag, doing
        so will tell the dialog this dialog was invoked from to close itself
        """
        self.discard = 1
        self.done(1)

    def go_back(self):
        """
        Takes the user back to whatever they were editing by letting this
        dialog close.
        """
        self.done(1)

    def init_ui(self):
        # Set the window title
        self.setWindowTitle("Hold it!")

        # Creation
        self.mainLayout = QVBoxLayout()
        self.text = QLabel()
        self.buttonLayout = QHBoxLayout()
        self.backButton = QPushButton("Go Back")
        self.discardButton = QPushButton("Discard")

        text = '' # An empty text string to be put in a label later

        if self.dialog_type == 'recipe':
            text = (text + "Your recipe has missing information on it!")
        elif self.dialog_type == 'ingredient':
            text = (text + "Your ingredient has missing information on it!")
        elif self.dialog_type == 'instruction':
            text = (text + "You did not input an instruction, try again!")
        else:
            # This isn't supposed to happen
            print 'ERROR! Wrong dialog type passed to ErrorDialog'

        text = (text + " Click Go Back to go back and edit it again, or" +
                " click Discard to discard all changes made.")

        self.text.setText(text)
        self.text.setWordWrap(True)

        # Layouting
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.text)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.discardButton)
        self.mainLayout.addLayout(self.buttonLayout)

        # Signals
        self.backButton.clicked.connect(self.go_back)
        self.discardButton.clicked.connect(self.discard_item)

    def __init__(self, parent, dialog_type):
        super(ErrorDialog, self).__init__(parent)

        # A flag that determines whether the user wants to edit again or just
        # discard what they were doing
        self.discard = 0

        # Determines what kind of dialog this was invoked from
        self.dialog_type = dialog_type

        self.init_ui()
