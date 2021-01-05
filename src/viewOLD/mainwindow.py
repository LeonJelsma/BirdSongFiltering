import sys
import matplotlib

from src import util
from src.viewOLD.mplcanvas import MplCanvas
from PyQt5 import QtCore, QtWidgets

from src.wavfile import WavFile

matplotlib.use('Qt5Agg')


def run_ui():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(1280, 720)
    w.display_wav(util.open_wav("single_mono.wav"))
    app.exec_()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        #sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.show()

    def display_wav(self, wav: WavFile):
        sc = MplCanvas(self, width=5, height=4, dpi=100, wav_file=wav)
        self.setCentralWidget(sc)
