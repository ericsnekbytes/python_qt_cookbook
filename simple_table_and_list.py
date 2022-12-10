"""Qt Model/View feature demo app"""


import datetime
import os.path
import random
import sys

from PySide6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView, QTextEdit,
                               QSplitter, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView)


class WordPairModel(QAbstractTableModel):
    """When subclassing QAbstractTableModel, you must implement rowCount(), columnCount(), and data().
    Default implementations of the index() and parent() functions are provided by QAbstractTableModel.
    Well behaved models will also implement headerData()."""

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


class Person:
    """Simple demo class for storing person info"""

    def __init__(self, first, middle, last, age, height_mm):
        self.first = first
        self.middle = middle
        self.last = last
        self.age = age
        self.height_mm = height_mm


class PeopleModel(QAbstractTableModel):

    FIRST_NAME = 0
    MIDDLE_NAME = 1
    LAST_NAME = 2
    AGE = 3
    HEIGHT_MM = 4

    def __init__(self, user_data):
        super().__init__()

        # Store the data we're representing
        self.model_data = user_data

        # Assign numbers to Person attributes, so we can
        # associate them with different column numbers
        self.attrib_key = {
            # int: ['attrib_name', 'display_name']
            0: ['first', 'First Name'],
            1: ['middle', 'Middle Name'],
            2: ['last', 'Last Name'],
            3: ['age', 'Age'],
            4: ['height_mm', 'Height (mm)'],
        }

    def rowCount(self, parent):
        return len(self.model_data)

    def columnCount(self, parent):
        """The attrib_key holds the columns we want to show"""
        return len(self.attrib_key)

    def data(self, index, role):
        row = index.row()
        col = index.column()

        # Note that dicts are sorted in Py3.7+, so here
        # we just index an ordered list of our dict items
        if index.isValid():
            if role == Qt.DisplayRole:
                person = self.model_data[row]
                attrib_name, display_val = self.attrib_key[col]

                return str(getattr(person, attrib_name))

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
                attrib_name, display_val = self.attrib_key[section]

                return display_val


class PeopleSortFilterModel(QSortFilterProxyModel):
    """Lets us sort/filter a PeopleModel"""

    def __init__(self, user_data):
        super().__init__()

        self.model_data = user_data
        self.setSourceModel(user_data)
        self.filter_string = ''

    def filterAcceptsRow(self, source_row, source_parent):
        if self.filter_string:
            index = self.model_data.index(source_row, PeopleModel.FIRST_NAME)
            first_name = self.model_data.data(index, Qt.DisplayRole)

            return True if first_name.lower().startswith(self.filter_string) else False

        # If no filter, all rows are accepted
        return True

    def filterAcceptsColumn(self, source_column, source_parent):
        return True

    def set_filter_string(self, user_filter):
        self.filter_string = user_filter

        # Tell Qt to invalidate the model and re-query
        self.beginResetModel()
        self.endResetModel()

    def lessThan(self, source_left, source_right):
        # If you want to customize sort behavior, do the comparison logic here
        left = self.model_data.data(source_left, Qt.DisplayRole)
        right = self.model_data.data(source_right, Qt.DisplayRole)

        return left < right


class CustomWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Internal data that we want to display in a table
        self.word_pairs = {
            'fruit': 'banana',
            'vegetable': 'spinach',
            'animal': 'dog',
            'mineral': 'quartz',
        }

        # Set some initial properties
        layout = QVBoxLayout()
        self.setWindowTitle('Sample tables and lists')
        self.setLayout(layout)

        # Start defining an area that will hold a
        # table layout for our word pairs
        layout.addWidget(QLabel('Word pairs, in a table:'))

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

        # Make a list of people, then show it in a sortable table
        people = [
            Person('Alice', 'Lee', 'Smith', 33, 181),
            Person('Aaron', 'Jake', 'Bell', 29, 177),
            Person('Bob', 'Greg', 'Candler', 24, 193),
            Person('Ben', 'Joseph', 'Wicket', 34, 174),
            Person('William', 'Troy', 'Ackford', 49, 207),
            Person('Walter', 'Sam', 'Beckett', 57, 202),
            Person('Megan', 'Rose', 'Rust', 11, 180),
            Person('Mark', 'Charles', 'Ford', 16, 172),
            Person('Jeff', 'Glenn', 'Teesdale', 71, 179),
            Person('Jessica', 'Lala', 'Earl', 45, 212),
            Person('Nancy', 'Elizabeth', 'Lemon', 40, 211),
        ]
        self.people = people

        # Show a header for the people table area
        layout.addWidget(QLabel('People, in a table'))
        # ...........................................
        # Show a filter field and button for the people table
        people_controls = QHBoxLayout()
        layout.addLayout(people_controls)
        # ...............................
        people_filter_field = QLineEdit()
        people_filter_field.setPlaceholderText(
            'First-name-starts-with'
        )
        people_controls.addWidget(people_filter_field)
        self.people_filter_field = people_filter_field
        # ............................................
        people_filter_btn = QPushButton('Filter People')
        people_filter_btn.clicked.connect(self.handle_apply_people_filter)
        people_controls.addWidget(people_filter_btn)
        # ..........................................
        clear_people_filt_btn = QPushButton('Clear Filter')
        clear_people_filt_btn.clicked.connect(self.handle_clear_people_filter)
        people_controls.addWidget(clear_people_filt_btn)

        # Make a model for our People
        people_model = PeopleModel(people)
        self.people_model = people_model
        # Make a sort/filter proxy model, it enabled us to
        # inform Qt about which items from the original model
        # are filtered out and how they should be sorted
        people_sort_model = PeopleSortFilterModel(people_model)
        self.people_sort_model = people_sort_model

        # A table view of our people
        people_table = QTableView()
        people_table.setModel(people_sort_model)
        # Set extra table settings
        people_table.setSortingEnabled(True)
        # Only allow single, full-row selections
        people_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        people_table.setSelectionMode(QAbstractItemView.SingleSelection)
        # Set header behaviors
        # ....................
        # Make the last column fit the parent layout width
        horiz_header = people_table.horizontalHeader()
        horiz_header.setStretchLastSection(True)
        vert_header = word_table.verticalHeader()
        vert_header.setSectionResizeMode(QHeaderView.Fixed)
        # ..........................
        layout.addWidget(people_table)
        self.people_table = people_table

        # Size the widget after adding stuff to the layout
        self.resize(900, 600)
        self.people_table.resizeColumnsToContents()
        # Make sure you show() the widget!
        self.show()

    def handle_apply_people_filter(self):
        self.people_sort_model.set_filter_string(self.people_filter_field.text().lower())

    def handle_clear_people_filter(self):
        self.people_filter_field.clear()
        self.people_sort_model.set_filter_string('')


def run_gui():
    """Function scoped main app entrypoint"""
    # Start the QApplication!
    app = QApplication(sys.argv)

    # This widget shows itself (the main GUI entrypoint)
    my_widget = CustomWidget()

    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
