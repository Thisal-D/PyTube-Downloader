from widgets.pyside6 import MainWindow
import sys

import qt_material
from PySide6 import QtWidgets



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # 设置样式表
    qt_material.apply_stylesheet(app, theme="dark_teal.xml")
    # 标题
    app.setApplicationName("PyTube Downloader")

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())