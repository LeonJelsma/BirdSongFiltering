#Entry point
import sys

from PyQt5 import QtWidgets

from src import const, util
from src.ui.mainWindow import MainWindow

single = util.open_wav("single_mono.wav")
#util.write_wav(single)


def filter2(x):
    y = [0]*len(x)
    for n in range(2, len(x)):
        y[n] = round(x[n] - x[n-1] - 0.2217*x[n-1] + 0.2217*x[n-2] + 0.2217*y[n-1])
    return y


single.data = filter2(single.data)

util.write_wav(single)

#app = QtWidgets.QApplication(sys.argv)
#window = MainWindow()
#app.exec_()