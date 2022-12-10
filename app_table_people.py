"""Shows people in a table.

This demo shows a table with some editing features. This builds
upon the simpler app_table_word_pairs example, and shows how
to use a QAbstractTableModel to edit an underlying data source.
"""


import re
import sys

from PySide6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView,
                               QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView,
                               QStyledItemDelegate)


class Person:
    """Simple demo class for storing person info"""

    def __init__(self, first, middle, last, age, height_mm):
        self.first = first
        self.middle = middle
        self.last = last
        self.age = age
        self.height_mm = height_mm


class PeopleModel(QAbstractTableModel):
    """Tells Qt how our person data corresponds to different rows/columns/cells.

    From the Qt documentation:
      When subclassing QAbstractTableModel, you must implement rowCount(),
      columnCount(), and data(). Default implementations of the index()
      and parent() functions are provided by QAbstractTableModel.
      Well behaved models will also implement headerData().

      Editable models need to implement setData(), and implement flags() to
      return a value containing Qt::ItemIsEditable.

      Models that provide interfaces to resizable data structures can provide
      implementations of insertRows(), removeRows(), insertColumns(),
      and removeColumns().
    """

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
        """Count how many attribs we're showing in attrib_key"""
        return len(self.attrib_key)

    def data(self, index, role):
        row = index.row()
        col = index.column()

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

    def setData(self, index, value, role):
        row = index.row()
        col = index.column()

        if index.isValid():
            if role == Qt.DisplayRole:
                person = self.model_data[row]
                attrib_name, display_val = self.attrib_key[col]
                stripped = value.strip()

                # Age and height are numbers, convert if needed
                if col in {PeopleModel.AGE, PeopleModel.HEIGHT_MM}:
                    if re.match(r'[0-9]+', stripped):
                        setattr(person, attrib_name, int(stripped))

                        self.dataChanged.emit(index, index, [Qt.DisplayRole])
                        return True
                else:
                    # Names are strings, just store them
                    setattr(person, attrib_name, stripped)

                    self.dataChanged.emit(index, index, [Qt.DisplayRole])
                    return True

        # The item was not edited, return False
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


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

        # This tells Qt to invalidate the model, which will cause
        # connected views to refresh/re-query any displayed data
        self.beginResetModel()
        self.endResetModel()

    def lessThan(self, source_left, source_right):
        # If you want to customize sort behavior, do the comparison logic here
        left = self.model_data.data(source_left, Qt.DisplayRole)
        right = self.model_data.data(source_right, Qt.DisplayRole)

        return left < right


class PeopleFieldEditor(QLineEdit):
    """Provides a QLineEdit that only allows digit entry on numeric fields"""

    def __init__(self, parent, column):
        super().__init__(parent)

        # Store the column type (age and height are numeric columns)
        self.column = column

    def keyPressEvent(self, event):
        # Restrict accepted keypresses if this editor is for a numeric column
        if self.column in {PeopleModel.AGE, PeopleModel.HEIGHT_MM}:
            event.accept()

            accepted_keys = {
                # Accept digits
                Qt.Key_0,
                Qt.Key_1,
                Qt.Key_2,
                Qt.Key_3,
                Qt.Key_4,
                Qt.Key_5,
                Qt.Key_6,
                Qt.Key_7,
                Qt.Key_8,
                Qt.Key_9,
                # Also allow return/enter/tab and delete keys
                Qt.Key_Return,
                Qt.Key_Enter,
                Qt.Key_Tab,
                Qt.Key_Delete,
                Qt.Key_Backspace,
            }

            if event.key() in accepted_keys:
                event.ignore()
                super().keyPressEvent(event)
        else:
            # This editor is NOT for a numeric column,
            # let the editor do its normal thing
            event.ignore()
            super().keyPressEvent(event)


class PeopleDelegate(QStyledItemDelegate):
    """Provides editor widgets for editing the people table"""

    def __init__(self):
        super().__init__()

    def createEditor(self, parent, option, index):
        # You can create different widgets per column if you want,
        # but here we'll just use our PeopleFieldEditor for all cells
        row = index.row()
        col = index.column()

        return PeopleFieldEditor(parent, col)

    def setEditorData(self, editor, index):
        # This populates the contents of the editor based on the index
        # (so our line editor will be pre-populated with names, for instance)
        editor.setText(index.model().data(index, Qt.DisplayRole))

    def setModelData(self, editor, model, index):
        # This attempts to assign the new value given by the editor
        model.setData(index, editor.text(), Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        """Just call the superclass implementation here"""
        # Let Qt size and position the editor widget, you probably
        # don't want to manually size and position the widget yourself
        super().updateEditorGeometry(editor, option, index)


class CustomWidget(QWidget):
    """A widget that shows people in a table"""

    def __init__(self):
        super().__init__()

        # Set some initial properties
        layout = QVBoxLayout()
        self.setWindowTitle('Some people, in a table')
        self.setLayout(layout)

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
        # Make a sort/filter proxy model, it enables us to
        # inform Qt about which items from the original model
        # are filtered out and how they should be sorted
        people_sort_model = PeopleSortFilterModel(people_model)
        self.people_sort_model = people_sort_model

        # A table view of our people
        people_table = QTableView()
        people_table.setModel(people_sort_model)
        people_table.setItemDelegate(PeopleDelegate())
        # Set extra table settings
        # ..................................
        people_table.setSortingEnabled(True)
        # Only allow single, full-row selections
        people_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        people_table.setSelectionMode(QAbstractItemView.SingleSelection)
        # Set header behaviors
        # ....................
        # Make the last column fit the parent layout width
        horiz_header = people_table.horizontalHeader()
        horiz_header.setStretchLastSection(True)
        vert_header = people_table.verticalHeader()
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
    # Initialize the QApplication!
    app = QApplication(sys.argv)

    # This widget shows itself (the main GUI entrypoint)
    my_widget = CustomWidget()

    # Run the program/start the event loop with exec()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
