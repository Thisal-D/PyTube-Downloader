from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .add_toolbar import AddToolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.removeToolBar(self.toolbar)
        self.set_toolbar()
        self.set_ui()
        # self.setCentralWidget(
        #     QPushButton(
        #         text="哈哈"
        #     )
        # )

    def set_toolbar(self):
        # 隐藏标题栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.toolbar = AddToolbar()
        self.toolbar.btn_max.clicked.connect(self.window_max)
        self.toolbar.btn_min.clicked.connect(self.showMinimized)
        self.toolbar.btn_close.clicked.connect(self.close)
        self.toolbar.mouseMoveEvent = self.move_title_bar

        self.addToolBar(self.toolbar)


    def move_title_bar(self, event):
        """
        拖动顶部标题条
        :param event:
        :return:
        """
        self.windowHandle().startSystemMove()

    def window_max(self):
        if self.isMaximized():
            self.showNormal()
            self.toolbar.btn_max.setIcon(QIcon("assets/ui images/max-normal.svg"))
        else:
            self.showMaximized()
            self.toolbar.btn_max.setIcon(QIcon("assets/ui images/max-max.svg"))

        self.toolbar.btn_max.clearFocus()

    def set_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(self.set_download_line())
        layout.addWidget(self.set_state_bar())
        layout.addWidget(self.set_list())

        layout.addStretch()

        self.setCentralWidget(widget)

    def set_download_line(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        btn_logo = QPushButton(text="", icon=QIcon("assets/main icon/64x64.ico"))
        text_line = QLineEdit()
        text_line.setPlaceholderText("Enter Youtube Url")
        text_line.setStyleSheet("color:white;")

        layout.addWidget(btn_logo)
        layout.addWidget(text_line)

        widget_model = QWidget()
        layout_model = QVBoxLayout()

        self.model = QRadioButton()
        self.model.setChecked(True)

        layout_model.addWidget(self.model)

        layout.addWidget(widget_model)

        btn_add = QPushButton("Add +")
        layout.addWidget(btn_add)
        return widget

    def set_state_bar(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        def _show_added():
            ...

        def _show_download():
            ...

        def _show_downloaded():
            ...

        btn_added = QPushButton("Added ({})")
        btn_download = QPushButton("Download ({})")
        btn_downloaded = QPushButton("Downloaded ({})")

        layout.addWidget(btn_added)
        layout.addWidget(btn_download)
        layout.addWidget(btn_downloaded)

        return widget

    def set_list(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        layout.addStretch()
        return widget
