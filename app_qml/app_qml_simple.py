"""Sample QML app"""


import datetime
import os.path
import random
import sys
import traceback

from PySide6.QtCore import Qt, Signal, QSize, QUrl, QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtQuickControls2 import QQuickStyle


class BackendObject(QObject):

    def __init__(self):
        super().__init__()

    # Mark methods you want to call from QML with the @Slot decorator,
    # and use the result= keyword arg to specify the return type
    @Slot(str, result=str)
    def pronk(self, path):
        if path.startswith('file:///'):
            path = path[len('file:///'):]
        print('[Py Backend] Received "{}"'.format(path))
        if os.path.exists(path):
            try:
                with open(path, 'rb') as fhandle:
                    data = fhandle.read()
                    if not data:
                        print('[Py Backend] File was empty')
                    return data.hex()[:64]
            except Exception as err:
                traceback.print_exc()
                print("\n[PyBackend] Couldn't read the specified file")
        else:
            print('\n[PyBackend] File does not appear to exist')
            return ''


def run_gui():
    """Function scoped main app entrypoint"""
    # Initialize the QApplication!
    app = QGuiApplication(sys.argv)

    # Use QQuickStyle to select "Universal" theme
    style = QQuickStyle()
    style.setStyle('Universal')

    # Show the rootwindow
    view = QQuickView()
    view.setTitle('Demo QML app')
    view.setSource(QUrl.fromLocalFile('rootwindow.qml'))
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()

    # You can expose Python code to your QML files with the
    # QML context (this lets embedded Javascript in your QML
    # files call Python functions defined in this app)
    context = view.rootContext()
    backend = BackendObject()
    context.setContextProperty('python_backend', backend)

    # Run the program/start the event loop with exec()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()
