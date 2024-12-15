from PySide6.QtGui import *
from PySide6.QtWidgets import *


class AddToolbar(QToolBar):
    def __init__(self):
        # 设置自定义标题栏
        super().__init__()
        self.setMovable(False)


        widget_filling = QWidget()
        self.addWidget(widget_filling)
        layout = QHBoxLayout(widget_filling)

        self.btn_logo = QPushButton(text="", icon=QIcon("assets/main icon/64x64.ico"))
        self.btn_logo.setFlat(True)
        layout.addWidget(self.btn_logo)

        self.btn_home = QPushButton(text="", icon=QIcon("assets/ui images/home.svg"))
        self.btn_home.setFlat(True)
        layout.addWidget(self.btn_home)

        layout.addStretch()

        self.btn_min = QPushButton(text="", icon=QIcon("assets/ui images/min.svg"))
        self.btn_max = QPushButton(text="", icon=QIcon("assets/ui images/max-normal.svg"))
        self.btn_close = QPushButton(text="", icon=QIcon("assets/ui images/close.svg"))
        #
        self.btn_min.setFlat(True)
        self.btn_max.setFlat(True)
        self.btn_close.setFlat(True)
        #
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)


