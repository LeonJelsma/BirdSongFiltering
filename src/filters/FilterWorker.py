import threading

from PyQt5.QtCore import QThread, QObject, pyqtSlot
from PyQt5 import QtCore

from filters.audiofilter import AudioFilter
from wavfile import WavFile


class FilterWorker(QObject):
    finished = QtCore.pyqtSignal(WavFile)
    started = QtCore.pyqtSignal()

    def __init__(self, wav: WavFile, min_freq, max_freq, audio_filter: AudioFilter):
        super(FilterWorker, self).__init__()
        self.wav = wav
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.audio_filter = audio_filter

    @pyqtSlot()
    def run(self):
        result = self.audio_filter.filter(min_freq=self.min_freq, max_freq=self.max_freq, wav=self.wav)
        self.finished.emit(result)
