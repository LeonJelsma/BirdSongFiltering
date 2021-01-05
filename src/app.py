#Entry point
import sys

import numpy
from PyQt5.QtWidgets import QApplication
from src.ui.mainWindow import MainWindow

#single = util.open_wav("single_mono.wav")
#util.write_wav(single)


def filter2(x):
    x = numpy.fromstring(x, "Int16")
    y = [0]*len(x)
    for n in range(2, len(x)):
        y[n] = int(round(x[n] - x[n-1] - 0.2217*x[n-1] + 0.2217*x[n-2] + 0.2217*y[n-1]))
    return y


#single.data = filter2(single.data)

#util.write_wav(single)

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
