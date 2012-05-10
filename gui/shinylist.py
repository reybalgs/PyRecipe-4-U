#!/usr/bin/python

import sys
from PySide.QtCore import *
from PySide.QtGui import *

# ShinyList code is based on code from:
# http://qt-articles.blogspot.com/2010/07/how-to-customize-listview-in-qt-using.html
#
# Ported to Python, made more object-oriented, and tweaked - the pixel offsets
# used by the C++ code resulted in misplaced labels and icons in Python.

# This code was reused from an early version of our INTROSE project.
# The primary author of this file is Lawrence Patrick Calulo.

class ShinyListDelegate(QStyledItemDelegate):
    """
    ShinyListDelegate implements the enhanced list items that are used with
    ShinyList. This class should *not* be used outside of the ShinyList
    implementation itself.

    See ShinyList and ShinyListItem for details on using a ShinyList.
    """
    HeaderTextRole = Qt.UserRole + 100
    SubHeaderTextRole = Qt.UserRole + 101
    IconRole = Qt.UserRole + 102

    def sizeHint(self, option, index):
        icon = index.data(self.IconRole) or QIcon()
        iconSize = icon.actualSize(option.decorationSize)
        iconSize.setWidth(32)
        iconSize.setHeight(32)
        font = QApplication.font()
        fm = QFontMetrics(font)

        return (QSize(iconSize.width(), iconSize.height() + fm.height() + 8))

    def paint(self, painter, option, index):
        super(ShinyListDelegate, self).paint(painter, option, index)

        painter.save()

        mainFont = QApplication.font()
        subFont = QApplication.font()

        mainFont.setBold(True)
        subFont.setWeight(subFont.weight() - 2)
        fm = QFontMetrics(mainFont)
        
        icon = index.data(self.IconRole) or QIcon()
        headerText = index.data(self.HeaderTextRole)
        subText = index.data(self.SubHeaderTextRole)

        iconSize = icon.actualSize(option.decorationSize)

        headerRect = option.rect
        subHeaderRect = option.rect
        iconRect = subHeaderRect

        iconRect.setRight(iconSize.width() + 30)
        iconRect.setTop(iconRect.top() + 5)
        headerRect.setLeft(iconRect.right())
        subHeaderRect.setLeft(iconRect.right())
        headerRect.setTop(headerRect.top() + 5)
        headerRect.setBottom(headerRect.top() + fm.height())

        subHeaderRect.setTop(headerRect.bottom() + 2)

        painter.drawPixmap(
            QPoint(iconRect.left() - 40,
                iconRect.top() - 20),
            icon.pixmap(iconSize.width(), iconSize.height()))

        painter.setFont(mainFont)
        painter.drawText(headerRect.left(), headerRect.top() - 7, headerText)

        painter.setFont(subFont)
        painter.drawText(subHeaderRect.left(), subHeaderRect.top() + 14, subText)

        painter.restore()


class ShinyListItem(QStandardItem):
    """
    A ShinyListItem is an element of a ShinyList. It has an icon, a main text, and
    a sub-text.

    Instances of this class can be added to a ShinyList, which would then display
    the item's data.
    """
    def __init__(self):
        super(ShinyListItem, self).__init__()
        self.setEditable(False)

    def set_main_text(self, text):
        """
        Sets the main text of the ShinyListItem, i.e. the bold text in its top half
        """
        self.setData(text, ShinyListDelegate.HeaderTextRole)
    
    def set_sub_text(self, text):
        """
        Sets the sub-text of the ShinyListItem, i.e. the less emphasized text in its
        bottom half
        """
        self.setData(text, ShinyListDelegate.SubHeaderTextRole)

    def set_icon(self, icon):
        """
        Sets the item's icon
        """
        self.setData(icon, ShinyListDelegate.IconRole)

    def get_main_text(self):
        """
        Returns the main text of the shinylist item.
        """
        return self.data(ShinyListDelegate.HeaderTextRole)

    def get_sub_text(self):
        """
        Returns the sub text of the shinylist item.
        """
        return self.data(ShinyListDelegate.HeaderTextRole)


class ShinyList(QListView):
    """
    A ShinyList is a special list widget, which allows items with an icon and two text
    labels. ShinyListItems can be added to it, which in turn will make a corresponding
    row appear in the GUI.
    """
    def __init__(self, parent=None):
        super(ShinyList, self).__init__(parent)
        delegate = ShinyListDelegate()
        self.model = QStandardItemModel()
        self.setItemDelegate(delegate)
        self.setModel(self.model)

    def add_item(self, item):
        self.model.appendRow(item)

    def remove_item(self, item):
        if isinstance(item, int):
            self.model.takeRow(item)
        else:
            self.model.takeRow(item.index())

    def clear(self):
        self.model.clear()


def main():
    app = QApplication(sys.argv)    
    slist = ShinyList()

    mainTextEdit = QLineEdit('The quick brown fox')
    subTextEdit = QLineEdit('It jumps over the lazy dog.')
    
    window = QWidget()
    layout = QVBoxLayout()
    
    button = QPushButton("Add Items")
    button.show()
    
    def on_button_clicked():
        item = ShinyListItem()
        itemMainText = mainTextEdit.text()        # Maintext for a ShinyListItem
        item.set_main_text(itemMainText)
        
        itemSubText = subTextEdit.text()          # Subtext for a ShinyListItem
        item.set_sub_text(itemSubText)

        slist.add_item(item)                    # Outputs a line of ShinyListItem

    button.clicked.connect(on_button_clicked)
    
    layout.addWidget(slist)        
    layout.addWidget(button)
    layout.addWidget(mainTextEdit)
    layout.addWidget(subTextEdit)
    
    window.setLayout(layout)
    window.show()
        
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

