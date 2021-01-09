import concurrent
import os

import numpy
import numpy as np
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from PyQt5.QtGui import QMovie, QColor

from PyQt5.QtWidgets import QFileDialog, QGraphicsView, QMessageBox
from wrapt import synchronized
from src import const, util
from src.filters import filters, butterworth_filter
from src.filters.FilterThread import FilterThread
from src.filters.audiofilter import AudioFilter
from src.wavfile import WavFile

FILTERS = {
    "Butterworth": filters.get_butterworth_filter,
    "FTT": filters.get_fft_filter
}


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi(util.get_ui_file("mainWindow.ui"), self)
        #self.setStyleSheet(open(util.get_style("light.qss")).read())
        self.setWindowTitle("Bird song recognizer")
        self.selectedFileDisplay.setText("Please select a file...")
        self.selectFileButton.clicked.connect(self.open_file_dialog)

        self.save_wav_button.clicked.connect(self.save_filtered_result)
        self.use_as_input_button.clicked.connect(self.use_result_as_input)
        self.autoRangeUnfiltered.clicked.connect(self.auto_range_unfiltered)
        self.autoRangeFiltered.clicked.connect(self.auto_range_filtered)
        self.resetButton.clicked.connect(self.clear_graphs)
        self.statusLabel.setText("No task")

        self.selected_filter = FILTERS["Butterworth"]
        self.filter_selection.activated[str].connect(self.on_change_filter)
        for name, function in FILTERS.items():
            self.filter_selection.addItem(name)

        self.bottom_freq_input.setPlainText("3000")
        self.top_freq_input.setPlainText("8000")

        self.unfilteredGraph.setMouseEnabled(x=False, y=False)
        self.filteredGraph.setMouseEnabled(x=False, y=False)

        spinner = self.waitingSpinner
        spinner.setRoundness(70.0)
        spinner.setMinimumTrailOpacity(15.0)
        spinner.setTrailFadePercentage(70.0)
        spinner.setNumberOfLines(12)
        spinner.setLineLength(10)
        spinner.setLineWidth(5)
        spinner.setInnerRadius(10)
        spinner.setRevolutionsPerSecond(1)
        spinner.setColor(QColor(86, 87, 86))
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.filter_wav)

        self.clear_graphs()
        self.show()

        self.filtered_wav: WavFile = None
        self.selected_wav: WavFile = None
        self.draw_unfiltered_graph()

    def on_change_filter(self, filter_name):
        self.selected_filter = FILTERS[filter_name]

    def open_file_dialog(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                const.AUDIO_DIR, "Wav files(*.wav)")
            self.update_selected_wav(fname[0])
        except PermissionError:
            print("Permission denied ):")

    def save_filtered_result(self):
        util.write_wav(self.filtered_wav)

    def use_result_as_input(self):
        self.selected_wav = self.filtered_wav
        self.clear_graphs()
        self.draw_filtered_graph()

    def clear_graphs(self):
        self.unfilteredGraph.setYRange(min=0, max=1)
        self.unfilteredGraph.setXRange(min=0, max=1)
        self.unfilteredGraph.setYRange(min=0, max=1)
        self.unfilteredGraph.setXRange(min=0, max=1)
        self.filteredGraph.clear()
        self.unfilteredGraph.clear()

    def update_selected_wav(self, file):
        path = os.path.normpath(file)
        file_name = os.path.basename(os.path.normpath(file))
        self.selected_wav = util.open_wav(path)
        if self.selected_wav.channels > 1:
            self.show_error_dialog("Selected file has more than 1 audio channel.")
            return
        self.selectedFileDisplay.setText(file_name)
        self.selectedFileDisplay.plainText = file_name
        if self.selected_wav:
            self.draw_unfiltered_graph()
            self.convertButton.setEnabled(True)
        else:
            self.convertButton.setEnabled(False)

    @staticmethod
    def show_error_dialog(message):
        error_window = QMessageBox()
        error_window.setIcon(QMessageBox.Information)

        error_window.setText("Error")
        error_window.setInformativeText(message)
        error_window.setWindowTitle("Error")
        error_window.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        error_window.exec_()

    def auto_range_unfiltered(self):
        self.unfilteredGraph.setYRange(min=-30000, max=30000)
        self.unfilteredGraph.setXRange(min=0, max=(self.selected_wav.frames / self.selected_wav.rate))

    def auto_range_filtered(self):
        self.filteredGraph.setYRange(min=-30000, max=30000)
        self.filteredGraph.setXRange(min=0, max=(self.selected_wav.frames / self.selected_wav.rate))

    def draw_unfiltered_graph(self):
        if self.selected_wav:
            data = np.fromstring(self.selected_wav.data, "Int16")
            time = np.arange(0, self.selected_wav.frames) * (1.0 / self.selected_wav.rate)

            self.unfilteredGraph.disableAutoRange()
            self.unfilteredGraph.plot(time, data)
            self.auto_range_unfiltered()
            self.unfilteredGraph.show()

    def filter_wav(self):
        min_freq = self.bottom_freq_input.toPlainText()
        max_freq = self.top_freq_input.toPlainText()
        self.waitingSpinner.start()
        self.statusLabel.setText("Filtering...")
        t = FilterThread(wav=self.selected_wav, min_freq=int(min_freq), max_freq=int(max_freq),
                         audio_filter=filters.get_butterworth_filter(),
                         return_func=self.set_filtered_data)
        t.start()

    @synchronized
    def set_filtered_data(self, wav):
        self.filtered_wav = wav
        self.draw_filtered_graph()
        self.statusLabel.setText("Done!")
        self.waitingSpinner.stop()

    def draw_filtered_graph(self):
        if self.filtered_wav:
            time = np.arange(0, self.filtered_wav.frames) * (1.0 / self.filtered_wav.rate)
            self.filteredGraph.plot(time, self.filtered_wav.data)
            self.auto_range_filtered()
            self.filteredGraph.show()
