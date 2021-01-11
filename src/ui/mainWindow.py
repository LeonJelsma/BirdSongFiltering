import concurrent
import os
import threading
from os.path import join

from PyQt5.QtCore import QThread

from algorithms import fft_algorithm
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QMovie, QColor
import pyqtgraph
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QComboBox
from PyQt5 import QtGui
from pyqtgraph import GraphicsLayoutWidget, QtCore, mkPen
from wrapt import synchronized
import const, util
from filters import filters
from filters.FilterWorker import FilterWorker
from plots import spectrogram
from plots import raw_audio
from wavfile import WavFile

FILTERS = {
    "Butterworth": filters.get_butterworth_filter,
    "FFT": filters.get_fft_filter
}

EXAMPLES = {}
for folder in [x[0] for x in os.walk(const.LABELED_BIRD_SOUNDS_DIR)]:
    if os.path.basename(folder) == 'labeled':
        continue
    EXAMPLES[os.path.basename(folder)] = folder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(util.get_ui_file("mainWindow.ui"), self)
        self.setWindowIcon(QtGui.QIcon(util.get_asset("icon.png")))
        self.setWindowTitle("Bird song recognizer")
        self.selectedFileDisplay.setText("Please select a file...")
        self.selectFileButton.clicked.connect(self.open_file_dialog)
        self.tab_view.setCurrentIndex(0)

        self.selected_example_1.activated[str].connect(
            lambda: self.on_change_example(widget=self.selected_example_spectrogram_1,
                                           name=self.selected_example_1.currentText()))
        self.selected_example_2.activated[str].connect(
            lambda: self.on_change_example(widget=self.selected_example_spectrogram_2,
                                           name=self.selected_example_2.currentText()))
        self.selected_example_3.activated[str].connect(
            lambda: self.on_change_example(widget=self.selected_example_spectrogram_3,
                                           name=self.selected_example_3.currentText()))

        index = 0
        for name, path in EXAMPLES.items():
            self.selected_example_1.addItem(name)
            self.selected_example_2.addItem(name)
            self.selected_example_3.addItem(name)
            if index == 0:
                index = self.selected_example_1.findText(name, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.selected_example_1.setCurrentIndex(index)
            elif index == 1:
                index = self.selected_example_2.findText(name, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.selected_example_2.setCurrentIndex(index)
            elif index == 2:
                index = self.selected_example_3.findText(name, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.selected_example_3.setCurrentIndex(index)
            index += 1

        self.on_change_example(widget=self.selected_example_spectrogram_1,
                               name=self.selected_example_1.currentText())

        self.on_change_example(widget=self.selected_example_spectrogram_2,
                               name=self.selected_example_2.currentText())

        self.on_change_example(widget=self.selected_example_spectrogram_3,
                               name=self.selected_example_3.currentText())

        self.save_wav_button.clicked.connect(self.save_filtered_result)
        self.use_as_input_button.clicked.connect(self.use_result_as_input)
        self.autoRangeUnfiltered.clicked.connect(self.auto_range_raw_audio_graph)
        self.autoRangeFiltered.clicked.connect(self.auto_range_magnitude_graphs)
        self.resetButton.clicked.connect(self.clear_graphs)
        self.statusLabel.setText("No task")

        self.selected_filter = FILTERS["Butterworth"]
        self.filter_selection.activated[str].connect(self.on_change_filter)
        for name, function in FILTERS.items():
            self.filter_selection.addItem(name)

        self.bottom_freq_input.setPlainText("3000")
        self.top_freq_input.setPlainText("8000")

        self.raw_audio_graph.setMouseEnabled(x=False, y=False)
        self.unfiltered_magnitude_graph.setMouseEnabled(x=False, y=False)
        self.filtered_magnitude_graph.setMouseEnabled(x=False, y=False)

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
        self.raw_audio_graph.addLegend()
        self.unfiltered_magnitude_graph.addLegend()
        self.filtered_magnitude_graph.addLegend()
        self.draw_unfiltered_graphs()
        self.filter_worker: FilterWorker = None
        self.thread: QThread = None

    @staticmethod
    def on_change_example(name, widget: GraphicsLayoutWidget):
        spectrogram.get_spectrogram(
            wav=util.open_wav(join(join(const.LABELED_BIRD_SOUNDS_DIR, EXAMPLES[name]), "1.wav")),
            graphics_layout=widget)

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
        self.draw_filtered_graphs()

    def clear_graphs(self):
        self.raw_audio_graph.setYRange(min=0, max=1)
        self.raw_audio_graph.setXRange(min=0, max=1)
        self.unfiltered_magnitude_graph.clear()
        self.filtered_magnitude_graph.clear()
        self.raw_audio_graph.clear()

    def update_selected_wav(self, file):
        self.clear_graphs()
        path = os.path.normpath(file)
        file_name = os.path.basename(os.path.normpath(file))
        self.selected_wav = util.open_wav(path)
        if self.selected_wav.channels > 1:
            self.show_error_dialog("Selected file has more than 1 audio channel.")
            return
        self.selectedFileDisplay.setText(file_name)
        self.selectedFileDisplay.plainText = file_name
        if self.selected_wav:
            self.draw_unfiltered_graphs()
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

    def auto_range_raw_audio_graph(self):
        self.raw_audio_graph.setYRange(min=-30000, max=30000)
        self.raw_audio_graph.setXRange(min=0, max=(self.selected_wav.frames / self.selected_wav.rate))

    def auto_range_magnitude_graphs(self):
        self.unfiltered_magnitude_graph.setXRange(min=0, max=self.selected_wav.frames)
        self.filtered_magnitude_graph.setXRange(min=0, max=self.selected_wav.frames)

    def draw_unfiltered_graphs(self):
        if self.selected_wav:
            data = np.fromstring(self.selected_wav.data, "Int16")
            time = np.arange(0, self.selected_wav.frames) * (1.0 / self.selected_wav.rate)
            # Raw audio graph
            self.raw_audio_graph.plot(x=time, y=data, pen=pyqtgraph.mkPen('b', width=1), name="Unfiltered")
            self.auto_range_raw_audio_graph()
            self.raw_audio_graph.show()

            # Magnitude graph
            dt = 1 / self.selected_wav.rate
            t = np.arange(0, len(data) / self.selected_wav.rate, dt)
            n = len(t)
            fhat = fft_algorithm.FFT_vectorized(data)
            PSD = fhat * np.conj(fhat) / n
            freq = (1 / (dt * n)) * np.arange(n)
            L = np.arange(1, np.floor(n / 2), dtype='int')
            y = freq[L]
            x = np.asarray(PSD[L], dtype='float')
            self.unfiltered_magnitude_graph.plot(freq[L], np.asarray(PSD[L], dtype='float'),
                                                 pen=pyqtgraph.mkPen('b', width=1), name="Unfiltered")

            # Spectrogram graph
            spectrogram.get_spectrogram(self.selected_wav, self.unfiltered_spectrogram)

    def filter_wav(self):
        min_freq = self.bottom_freq_input.toPlainText()
        max_freq = self.top_freq_input.toPlainText()
        self.waitingSpinner.start()
        self.statusLabel.setText("Filtering...")
        self.filter_worker = FilterWorker(wav=self.selected_wav, min_freq=int(min_freq), max_freq=int(max_freq),
                         audio_filter=filters.get_butterworth_filter())
        self.thread = QThread()
        self.filter_worker.moveToThread(self.thread)
        self.filter_worker.finished.connect(self.set_filtered_data)
        self.thread.started.connect(self.filter_worker.run)
        self.thread.start()

    def set_filtered_data(self, wav):
        self.filtered_wav = wav
        self.draw_filtered_graphs()
        self.statusLabel.setText("Done!")
        self.waitingSpinner.stop()

    def draw_filtered_graphs(self):
        if self.filtered_wav:
            time = np.arange(0, self.filtered_wav.frames) * (1.0 / self.filtered_wav.rate)
            # Raw audio
            self.raw_audio_graph.plot(x=time, y=self.filtered_wav.data, pen=pyqtgraph.mkPen('y', width=1),
                                      name="Filtered")
            # Magnitude graph
            dt = 1 / self.filtered_wav.rate
            t = np.arange(0, len(self.filtered_wav.data) / self.selected_wav.rate, dt)
            n = len(t)
            fhat = fft_algorithm.FFT_vectorized(self.filtered_wav.data)
            PSD = fhat * np.conj(fhat) / n
            freq = (1 / (dt * n)) * np.arange(n)
            L = np.arange(1, np.floor(n / 2), dtype='int')
            self.filtered_magnitude_graph.plot(freq[L], np.asarray(PSD[L], dtype='float'),
                                                 pen=pyqtgraph.mkPen('y', width=1), name="Unfiltered")

            self.raw_audio_graph.show()
            spectrogram.get_spectrogram(self.filtered_wav, self.filtered_spectrogram)
