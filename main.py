###############################################################################
#
# PyRecipe-4-U
#
# A cooking recipe management app, running on the PySide Qt Framework and
# written in Python
#
# Author: Aldo Rey Balagulan
#
# Copyright (C) 2012 Aldo Rey Balagulan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

# main.py
#
# Main program/file. Run this to run the entire program.

# Importing stuff
import simplejson as json # json imports
import sys

# GUI stuff
from gui.mainwindow import *

print 'Hello world!'

window = MainWindow()
sys.exit(app.exec_())
