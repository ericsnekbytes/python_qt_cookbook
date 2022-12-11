"""Basic word pairs table demo.

This demo shows a minimal example of how to display custom data
in a table interface. This involves using a QAbstractTableModel,
which tells Qt how your custom data corresponds to different
rows/columns/cells in the table, and a QTableView, which connects
to your table model to display your data to the user.
"""


import sys

from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableView, QLabel,
                               QHeaderView, QHBoxLayout, QPushButton)


class WordPairModel(QAbstractTableModel):
    """Tells Qt how our word pair data corresponds to different rows/columns/cells."""

    def __init__(self, user_data):
        super().__init__()

        # Store the data we're representing
        self.model_data = user_data

    def rowCount(self, parent):
        return len(self.model_data)

    def columnCount(self, parent):
        # This data (word pairs) always has 2 columns
        return 2

    def data(self, index, role):
        # So, data() does a lot of different things. This
        # function takes in a QModelIndex (which tells you
        # which cell/what data Qt needs info about), then
        # you respond by returning whatever KIND of information
        # Qt is looking for, determined by the role. Here are
        # the builtin roles Qt requests by default:
        #
        #   0) Qt::DisplayRole, 1) Qt::DecorationRole,
        #   2) Qt::EditRole 3) Qt::ToolTipRole, 4) Qt::StatusTipRole
        #   5) Qt::WhatsThisRole, 6) Qt::SizeHintRole
        #
        # Most of these you can probably ignore. Often, you
        # only need to provide data for the DisplayRole, which
        # will often just be some text representing your data...
        # but as you can see, for each cell, Qt also might want
        # to know how to size the data in that cell, or what
        # a good tooltip might be for the cell, etcetera. Make
        # SURE you specifically test for the roles that you care
        # about, and return None if the role isn't relevant to you.
        # Providing bad data/a nonsense return value for a role
        # you don't care about can make weird things happen.
        row = index.row()
        col = index.column()

        # Note that dicts are sorted in Py3.7+, so here
        # we just index an ordered list of our dict items
        if index.isValid():
            if role == Qt.DisplayRole:
                return list(self.model_data.items())[row][col]

        return None

    def headerData(self, section, orientation, role):
        # This is where you can name your columns, or show
        # some other data for the column and row headers
        if role == Qt.DisplayRole:
            # Just return a row number for the vertical header
            if orientation == Qt.Vertical:
                return str(section)

            # Return some column names for the horizontal header
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "First Word"
                if section == 1:
                    return "Second Word"

    def set_new_pair_data(self, user_data):
        # A custom function that clears the underlying word pair
        # data (and stores new data), then refreshes the model

        # Assign new underlying word pairs data
        self.model_data = user_data

        # This tells Qt to invalidate the model, which will cause
        # connected views to refresh/re-query any displayed data
        self.beginResetModel()
        self.endResetModel()


class CustomWidget(QWidget):
    """A widget that shows a simple table of word pairs

    From the Qt documentation:
      When subclassing QAbstractTableModel, you must implement rowCount(),
      columnCount(), and data(). Default implementations of the index()
      and parent() functions are provided by QAbstractTableModel.
      Well behaved models will also implement headerData().
    """

    def __init__(self):
        super().__init__()

        # Internal data that we want to display in a table
        self.word_pairs = {
            'fruit': 'banana',
            'vegetable': 'spinach',
            'animal': 'dog',
            'mineral': 'quartz',
            'nature': 'neat',
            'plant': 'tree',
            'yolk': 'yellow',
            'pillows': 'soft',
        }

        # Set some initial properties
        layout = QVBoxLayout()
        self.setWindowTitle('Basic table example')
        self.setLayout(layout)

        # Start defining an area that will hold a
        # table layout for our word pairs
        upper_area = QHBoxLayout()
        layout.addLayout(upper_area)
        upper_area.addWidget(QLabel('Word pairs, in a table:'))

        # Make a Qt model, this lets us use Qt's
        # standard table interface widget
        word_model = WordPairModel(self.word_pairs)
        self.word_model = word_model

        # A table view of the word_pairs dict
        word_table = QTableView()
        word_table.setModel(word_model)
        # Set header behaviors
        # ....................
        # Make the last column fit the parent layout width
        horiz_header = word_table.horizontalHeader()
        horiz_header.setStretchLastSection(True)
        vert_header = word_table.verticalHeader()
        vert_header.setSectionResizeMode(QHeaderView.Fixed)
        # ..........................
        layout.addWidget(word_table)
        self.word_table = word_table

        # Store an alternate word pair dict, then swap
        # back and forth between displaying the original and
        # the alternate in our word pair table
        alternate_word_pairs = {
            'sun': 'bright',
            'water': 'wet',
            'rocks': 'hard',
            'grass': 'soft',
            'planes': 'flying',
            'toast': 'golden',
        }
        self.alternate_word_pairs = alternate_word_pairs
        # Store which word pair dict is being shown now
        self.current_word_pairs = self.word_pairs

        # Make a button for swapping the displayed pairs
        swap_words_btn = QPushButton('Show Other Words')
        swap_words_btn.clicked.connect(self.handle_swap_words)
        upper_area.addStretch()
        upper_area.addWidget(swap_words_btn)

        # Size the widget after adding stuff to the layout
        self.resize(900, 600)
        # Size the table columns after resizing the main widget
        self.word_table.resizeColumnsToContents()
        # Make sure you show() the widget!
        self.show()

    def handle_swap_words(self):
        # Make the word_table show different data
        if self.current_word_pairs is self.word_pairs:
            # We're showing the original word pairs, switch to the alternates
            self.current_word_pairs = self.alternate_word_pairs
            self.word_model.set_new_pair_data(self.alternate_word_pairs)
        else:
            # We're showing the alternates, switch back to the original pairs
            self.current_word_pairs = self.word_pairs
            self.word_model.set_new_pair_data(self.word_pairs)

        # Resize the columns to fit the new contents
        self.word_table.resizeColumnsToContents()


def run_gui():
    """Function scoped main app entrypoint"""
    # Initialize the QApplication!
    app = QApplication(sys.argv)

    # This widget shows itself (the main GUI entrypoint)
    my_widget = CustomWidget()

    # Run the program/start the event loop with exec()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
