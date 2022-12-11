"""A very tiny app skeleton"""


import datetime
import random
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,
                               QHBoxLayout)


class CustomWidget(QWidget):
    """A very simple custom widget"""

    def __init__(self):
        super().__init__()

        # Set some initial properties
        layout = QVBoxLayout()
        self.setWindowTitle('Tiny sample app')
        self.setLayout(layout)

        # Add a text box
        text_area = QTextEdit()
        text_area.setAcceptRichText(False)
        msg = 'Hello! Type here, or hit "Time to Text"'
        text_area.setPlainText(msg)
        layout.addWidget(text_area)
        self.text_area = text_area

        # Some controls at the bottom of the window
        lower_row = QHBoxLayout()
        lower_row.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(lower_row)

        # Button for showing the time/some random data
        time_to_text_btn = QPushButton('Time to Text')
        # Add a tooltip (for on-hover)
        time_to_text_btn.setToolTip('Show a sample message in the text box')
        time_to_text_btn.clicked.connect(self.handle_press_time_to_text)
        lower_row.addStretch(1)  # Push the button to the right side
        lower_row.addWidget(time_to_text_btn)

        # Size the widget after adding stuff to the layout
        self.resize(900, 600)
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
        self.text_area.setPlainText(message)


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
