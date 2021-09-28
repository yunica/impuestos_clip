import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

def main():
    from src.main import MainWindow

    app = QApplication(sys.argv)
    mw = MainWindow()
    timer = QTimer()
    timer.timeout.connect(mw.old_montos_layout)
    timer.start(1000)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
