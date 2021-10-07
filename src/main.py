import sys
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QDesktopWidget,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QScrollBar,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTime
from src import constants
from pyperclip import copy
from functools import partial


class MainWindow(QWidget):
    universeChanged = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        # monto result
        self.ROUND_LIMIT = 10
        self.monto_result = QLabel()
        self.monto_result.setFont(QFont("Arial", 20))
        self.monto_result.setStyleSheet("text-align: right")
        self.monto_result.setAlignment(Qt.AlignRight)

        # monto
        self.monto_edit = QLineEdit()
        self.monto_edit.setMaxLength(10)
        self.monto_edit.setFont(QFont("Arial", 15))
        # old montos

        self.layout_montos = QVBoxLayout()
        self.old_montos = []

        self.initUI()

    def initUI(self):
        self.setGeometry(
            constants.GEOMETRY_LEFT,
            constants.GEOMETRY_TOP,
            constants.GEOMETRY_WIDTH,
            constants.GEOMETRY_HEIGHT,
        )
        self.setFixedSize(constants.GEOMETRY_WIDTH, constants.GEOMETRY_HEIGHT)
        self.setWindowTitle("Impuesto Copy")
        self.center()
        self.define_layout()
        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def define_layout(self):
        vlayour = QVBoxLayout()
        go_btn = QPushButton("go")
        go_btn.clicked.connect(self.calculate_monto_result)
        # event
        self.monto_edit.returnPressed.connect(go_btn.click)

        grid = QGridLayout()
        grid.setSpacing(constants.GRID_SPACING)
        # monto
        grid.addWidget(self.monto_edit, 1, 0, 1, 3)
        grid.addWidget(go_btn, 1, 3, 1, 1)
        # monto result
        self.monto_result.setText("00.00")
        grid.addWidget(self.monto_result, 2, 0, 2, 4)
        vlayour.addLayout(grid)

        vlayour.addLayout(self.layout_montos)
        vlayour.addStretch(1)
        self.setLayout(vlayour)

    def calculate_monto_result(self, monto_text=None):
        try:
            copy("-")
            if not monto_text:
                monto_text = self.monto_edit.text().strip()

            if not monto_text:
                raise Exception("no data")
            monto = round(float(monto_text) / 1.18, self.ROUND_LIMIT)
            copy(monto)
            self.monto_result.setText(str(monto))
        except Exception as ex:
            copy("-")
            print(ex.__str__())
            self.monto_result.setText("ingresa bien pe !")
            self.monto_edit.setText("")
        else:
            self.monto_edit.setText("")
            old_montos = list(self.old_montos)
            old_montos.append(monto_text)
            old_montos = list(dict.fromkeys(old_montos))
            self.old_montos = old_montos

    def old_montos_layout(self):
        time = QTime.currentTime().toString()
        # remove
        for i in reversed(range(self.layout_montos.count())):
            widgetToRemove = self.layout_montos.itemAt(i).widget()
            self.layout_montos.removeWidget(widgetToRemove)

        # border
        line = QLabel()
        line.setStyleSheet("border-top: 1px solid black;")
        self.layout_montos.addWidget(line)

        # add old monto
        for i in self.old_montos[::-1][:8]:
            go_btn = QPushButton(str(i))
            go_btn.clicked.connect(partial(self.calculate_monto_result, i))
            self.layout_montos.addWidget(go_btn)
        return time
