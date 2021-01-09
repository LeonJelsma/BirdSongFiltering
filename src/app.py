#Entry point
import sys
from PyQt5.QtWidgets import QApplication
from src.ui.mainWindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
