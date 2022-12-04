"""A simple, sample programmatic gui application in PySide2"""


import datetime
import random
import sys

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit,
                               QPushButton, QHBoxLayout, QSplitter, QLabel, QMessageBox)


class ChildWidget(QWidget):
    """A simple child widget of the main widget"""

    def __init__(self):
        super().__init__()

        # Set up some basics
        layout = QVBoxLayout()
        self.setWindowTitle('Cool child window')
        self.setLayout(layout)

        # Add a basic label
        layout.addWidget(QLabel('Status:'))

        # Add a read-only text box
        child_text = QTextEdit()
        child_text.setPlainText('EMPTY')
        child_text.setTextInteractionFlags(Qt.NoTextInteraction)
        layout.addWidget(child_text)
        self.child_text = child_text

        # Size after laying out
        self.resize(400, 300)

    def handle_incoming_mood(self, mood):
        """This is an example slot (a function) for mood change signals"""
        letters = [chr(codepoint) for codepoint in range(ord('A'), ord('A') + 26)]
        some_rand_letters = random.choices(population=letters, k=4)

        # Make a message with the mood and some random letters
        message = 'This window is {}\n\nRandom letters: {}'.format(
            mood,
            ''.join(some_rand_letters)
        )

        self.child_text.setPlainText(message)


class CustomWidget(QWidget):
    """A very simple custom widget"""

    # This is a basic custom signal
    mood_change = Signal(str)

    def __init__(self):
        super().__init__()

        # Set some initial properties
        layout = QVBoxLayout()
        self.setWindowTitle('Cool little sample app')
        self.setLayout(layout)

        # Add a main area with a draggable divider
        primary_area = QSplitter(orientation=Qt.Horizontal)
        layout.addWidget(primary_area)

        # Add a text box
        left_text_area = QTextEdit()
        left_text_area.setAcceptRichText(False)
        msg = 'Hello! Type here, or hit "Time to Text"'
        left_text_area.setPlainText(msg)
        primary_area.addWidget(left_text_area)
        self.left_text_area = left_text_area

        # Add a container widget with a horizontal layout
        right_control_area = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_control_area.setLayout(right_layout)
        primary_area.addWidget(right_control_area)

        # "Shout" button sample
        shout_lbl = QLabel('Some buttons')
        shout_btn = QPushButton('Shout')
        shout_btn.clicked.connect(self.handle_press_shout)
        right_layout.addWidget(shout_lbl)
        right_layout.addWidget(shout_btn)
        # Add a stretchable space to consume space at
        # the bottom of the layout (pushes other stuff up)
        right_layout.addStretch(1)
        self.shout_btn = shout_btn

        # Some controls at the bottom of the window
        lower_row = QHBoxLayout()
        lower_row.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(lower_row)

        # Button for showing the time/some random data
        time_to_text_btn = QPushButton('Time to Text')
        # Add a tooltip (for on-hover)
        time_to_text_btn.setToolTip('Show a sample message in the text box')
        time_to_text_btn.clicked.connect(self.handle_press_time_to_text)
        lower_row.addWidget(time_to_text_btn)
        lower_row.addStretch(1)  # Space the buttons apart

        # Hold a hidden child widget (separate window)
        child_widget = ChildWidget()
        # Connect the mood_change signal to the child's
        # handle_incoming_mood slot (basic signal/slot example)
        self.mood_change.connect(child_widget.handle_incoming_mood)
        self.child_widget = child_widget

        # Controls for the child window
        # .............................
        show_child_btn = QPushButton('Show child')
        show_child_btn.setToolTip('Show a child window')
        show_child_btn.clicked.connect(self.handle_show_child)
        lower_row.addWidget(show_child_btn)
        self.show_child_btn = show_child_btn
        # ..................................
        child_happy_btn = QPushButton('Make child happy')
        child_happy_btn.clicked.connect(self.handle_child_mood)
        lower_row.addWidget(child_happy_btn)
        self.child_happy_btn = child_happy_btn
        # ..................................
        child_confused_btn = QPushButton('Make child confused')
        child_confused_btn.clicked.connect(self.handle_child_mood)
        lower_row.addWidget(child_confused_btn)
        self.child_confused_btn = child_confused_btn

        # Size the widget after adding stuff to the layout
        self.resize(900, 600)
        primary_area.setSizes([2 * self.width() / 3, self.width() / 3])
        # Make sure you show() the widget!
        self.show()

    def handle_press_time_to_text(self):
        timestring = datetime.datetime.now().isoformat()
        letters = [chr(codepoint) for codepoint in range(ord('A'), ord('A') + 26)]
        some_rand_letters = random.choices(population=letters, k=4)

        message = 'The time is: {}\nRandom letters: {}\n'.format(
            timestring,
            ''.join(some_rand_letters)
        )
        self.left_text_area.setPlainText(message)

    def handle_press_shout(self):
        # Show a box with some shout options
        box = QMessageBox()
        box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        box.setWindowTitle('Shout Options')
        box.setText('Pick a shout')
        yes_btn = box.button(QMessageBox.Yes)
        yes_btn.setText('Shout YAY')
        no_btn = box.button(QMessageBox.No)
        no_btn.setText('Shout NAW')

        # Run the dialog/get the result
        result = box.exec_()

        # Show an info box with the result
        if result == QMessageBox.Yes:
            QMessageBox.information(
                self, 'Shouting', "I'm shouting YAY!!"
            )
        if result == QMessageBox.No:
            QMessageBox.information(
                self, 'Shouting', "I'm shouting NAW!!"
            )
        if result == QMessageBox.Cancel:
            QMessageBox.information(
                self, 'Canceled', 'You canceled the shout'
            )

    def handle_show_child(self):
        self.child_widget.show()

    def handle_child_mood(self):
        # Determine which button was clicked using self.sender(),
        # then emit the mood_change signal with a string (signals
        # are a main way of passing information around Qt)
        if self.sender() is self.child_happy_btn:
            self.mood_change.emit('HAPPY')
        if self.sender() is self.child_confused_btn:
            self.mood_change.emit('CONFUSED')


def run_gui():
    """Function scoped main app entrypoint"""
    # Start the QApplication!
    app = QApplication(sys.argv)

    # This widget shows itself (the main GUI entrypoint)
    my_widget = CustomWidget()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_gui()
