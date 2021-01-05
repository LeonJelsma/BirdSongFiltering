import os

from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtWidgets import QFileDialog

from src import const, util
from src.plots import frequencies


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(util.get_ui_file("mainWindow.ui"), self)
        self.setWindowTitle("Bird song recognizer")
        self.selectedFileDisplay.setText("Please select a file...")
        self.selectFileButton.clicked.connect(self.open_file_dialog)
        self.show()

        self.selectedWav = None

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            const.AUDIO_DIR, "Wav files(*.wav)")
        self.update_selected_wav(fname[0])

    def update_selected_wav(self, file):
        file_name = os.path.basename(os.path.normpath(file))
        self.selectedFileDisplay.setText(file_name)
        self.selectedFileDisplay.plainText = file_name

    def draw_unfiltered_graph(self):
        fig = frequencies.plot_spectogram(self.selectedWav, title=self.selectedWav.name)
