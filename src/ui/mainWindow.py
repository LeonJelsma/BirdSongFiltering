import os

import numpy as np
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg

from PyQt5.QtWidgets import QFileDialog, QGraphicsView

from src import const, util
from src.plots import frequencies
from src.wavfile import WavFile


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(util.get_ui_file("mainWindow.ui"), self)
        # self.setStyleSheet(open(util.get_style("light.qss")).read())
        self.setWindowTitle("Bird song recognizer")
        self.selectedFileDisplay.setText("Please select a file...")
        self.selectFileButton.clicked.connect(self.open_file_dialog)

        self.show()

        self.selectedWav: WavFile = None
        self.draw_unfiltered_graph()

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            const.AUDIO_DIR, "Wav files(*.wav)")
        self.update_selected_wav(fname[0])

    def update_selected_wav(self, file):
        file_name = os.path.basename(os.path.normpath(file))
        self.selectedWav = util.open_wav(file_name)
        self.selectedFileDisplay.setText(file_name)
        self.selectedFileDisplay.plainText = file_name
        self.draw_unfiltered_graph()

    def draw_unfiltered_graph(self):
        if self.selectedWav:
            print("test")
            #fig = frequencies.plot_spectogram(self.selectedWav, title=self.selectedWav.name)
            data = np.fromstring(self.selectedWav.data, "Int16")

            time = np.arange(0, self.selectedWav.frames) * (1.0 / self.selectedWav.rate)
            self.unfilteredGraph.plot(time, data)
            self.unfilteredGraph.show()
