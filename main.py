###############################################################################
#
# PyRecipe-4-U
#
# A cooking recipe management app, running on the PySide Qt Framework and
# written in Python
#
# Author: Aldo Rey Balagulan
#
###############################################################################

# main.py
#
# Main program/file. Run this to run the entire program.

# Importing stuff
import simplejson as json # json imports

# GUI stuff
from gui.mainwindow import *

print 'Hello world!'

window = MainWindow()
sys.exit(app.exec_())
