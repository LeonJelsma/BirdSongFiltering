import concurrent
import os

import numpy
import numpy as np
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from PyQt5.QtGui import QMovie, QColor

from PyQt5.QtWidgets import QFileDialog, QGraphicsView
from wrapt import synchronized
from src import const, util
from src.filters import filters
from src.filters.FilterThread import FilterThread
from src.wavfile import WavFile


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(util.get_ui_file("mainWindow.ui"), self)
        # self.setStyleSheet(open(util.get_style("light.qss")).read())
        self.setWindowTitle("Bird song recognizer")
        self.selectedFileDisplay.setText("Please select a file...")
        self.selectFileButton.clicked.connect(self.open_file_dialog)

        self.autoRangeUnfiltered.clicked.connect(self.auto_range_unfiltered)
        self.autoRangeFiltered.clicked.connect(self.auto_range_filtered)
        self.resetButton.clicked.connect(self.clear_graphs)
        self.statusLabel.setText("No task")
        spinner = self.waitingSpinner

        spinner.setRoundness(70.0)
        spinner.setMinimumTrailOpacity(15.0)
        spinner.setTrailFadePercentage(70.0)
        spinner.setNumberOfLines(12)
        spinner.setLineLength(10)
        spinner.setLineWidth(5)
        spinner.setInnerRadius(10)
        spinner.setRevolutionsPerSecond(1)
        spinner.setColor(QColor(81, 4, 71))
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.filter_wav)

        self.show()

        self.filteredData = None
        self.selectedWav: WavFile = None
        self.draw_unfiltered_graph()

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            const.AUDIO_DIR, "Wav files(*.wav)")
        self.update_selected_wav(fname[0])

    def clear_graphs(self):
        self.filteredGraph.clear()
        self.unfilteredGraph.clear()

    def update_selected_wav(self, file):
        file_name = os.path.basename(os.path.normpath(file))
        self.selectedWav = util.open_wav(file_name)
        self.selectedFileDisplay.setText(file_name)
        self.selectedFileDisplay.plainText = file_name
        if self.selectedWav:
            self.draw_unfiltered_graph()
            self.convertButton.setEnabled(True)
        else:
            self.convertButton.setEnabled(False)

    def auto_range_unfiltered(self):
        self.unfilteredGraph.setYRange(min=-30000, max=3000)
        self.unfilteredGraph.setXRange(min=0, max=(self.selectedWav.frames / self.selectedWav.rate))

    def auto_range_filtered(self):
        self.filteredGraph.setYRange(min=-30000, max=3000)
        self.filteredGraph.setXRange(min=0, max=(self.selectedWav.frames / self.selectedWav.rate))

    def draw_unfiltered_graph(self):
        if self.selectedWav:
            data = np.fromstring(self.selectedWav.data, "Int16")

            time = np.arange(0, self.selectedWav.frames) * (1.0 / self.selectedWav.rate)
            self.unfilteredGraph.plot(time, data)
            self.auto_range_unfiltered()
            self.unfilteredGraph.show()

    def filter_wav(self):
        self.waitingSpinner.start()
        self.statusLabel.setText("Filtering...")
        t = FilterThread(data=self.selectedWav.data, filter_func=filters.filter3, return_func=self.set_filtered_data)
        t.start()

    @synchronized
    def set_filtered_data(self, data):
        self.filteredData = data
        self.draw_filtered_graph()
        self.statusLabel.setText("Done!")
        self.waitingSpinner.stop()

    def draw_filtered_graph(self):
        if self.selectedWav:
            time = np.arange(0, self.selectedWav.frames) * (1.0 / self.selectedWav.rate)
            self.filteredGraph.plot(time, self.filteredData)
            self.auto_range_filtered()
            self.filteredGraph.show()

