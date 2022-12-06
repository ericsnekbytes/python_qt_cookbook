"""Qt Model/View feature demo app"""


import datetime
import os.path
import random
import sys

from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView, QTextEdit)


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

        # A view of the word_associations dict
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

        layout.addWidget(QTextEdit())

        # Size the widget after adding stuff to the layout
        self.resize(900, 600)
        # Make sure you show() the widget!
        self.show()

    # def handle_press_time_to_text(self):
    #     timestring = datetime.datetime.now().isoformat()
    #     letters = [chr(codepoint) for codepoint in range(ord('A'), ord('A') + 26)]
    #     some_rand_letters = random.choices(population=letters, k=4)
    #
    #     message = 'The time is: {}\nRandom letters: {}\n'.format(
    #         timestring,
    #         ''.join(some_rand_letters)
    #     )
    #     self.left_text_area.setPlainText(message)
    #
    # def handle_press_shout(self):
    #     # Show a box with some shout options
    #     box = QMessageBox()
    #     box.setStandardButtons(
    #         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
    #     )
    #     box.setWindowTitle('Shout Options')
    #     box.setText('Pick a shout')
    #     yes_btn = box.button(QMessageBox.Yes)
    #     yes_btn.setText('Shout YAY')
    #     no_btn = box.button(QMessageBox.No)
    #     no_btn.setText('Shout NAW')
    #
    #     # Run the dialog/get the result
    #     result = box.exec()
    #
    #     # Show another info box with the result
    #     if result == QMessageBox.Yes:
    #         QMessageBox.information(
    #             self, 'Shouting', "I'm shouting YAY!!"
    #         )
    #     if result == QMessageBox.No:
    #         QMessageBox.information(
    #             self, 'Shouting', "I'm shouting NAW!!"
    #         )
    #     if result == QMessageBox.Cancel:
    #         QMessageBox.information(
    #             self, 'Canceled', 'You canceled the shout'
    #         )
    #
    # def handle_pick_file(self):
    #     filepath, filefilter = QFileDialog.getOpenFileName(self)
    #
    #     if filepath:
    #         self.file_picker_result_field.setText(os.path.basename(filepath))
    #     else:
    #         self.file_picker_result_field.clear()
    #
    # def handle_food_check(self, state):
    #     meal_type = ''
    #     if self.sender() is self.breakfast_cb:
    #         meal_type = 'breakfast'
    #     if self.sender() is self.lunch_cb:
    #         meal_type = 'lunch'
    #     if self.sender() is self.dinner_cb:
    #         meal_type = 'dinner'
    #
    #     if state:
    #         QMessageBox.information(
    #             self,
    #             'Meal updated!',
    #             '{} will be served.'.format(meal_type.title())
    #         )
    #     else:
    #         QMessageBox.information(
    #             self,
    #             'Meal updated!',
    #             'Canceling {}.'.format(meal_type)
    #         )
    #
    # def handle_show_child(self):
    #     self.child_widget.show()
    #
    # def handle_child_mood(self):
    #     # Determine which button was clicked using self.sender(),
    #     # then emit the mood_change signal with a string (signals
    #     # are a main way of passing information around Qt)
    #     if self.sender() is self.child_happy_btn:
    #         self.mood_change.emit('HAPPY')
    #     if self.sender() is self.child_confused_btn:
    #         self.mood_change.emit('CONFUSED')


def run_gui():
    """Function scoped main app entrypoint"""
    # Start the QApplication!
    app = QApplication(sys.argv)

    # This widget shows itself (the main GUI entrypoint)
    my_widget = CustomWidget()

    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
