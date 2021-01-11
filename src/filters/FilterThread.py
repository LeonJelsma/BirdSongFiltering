import threading

from filters.audiofilter import AudioFilter
from wavfile import WavFile


class FilterThread(threading.Thread):

    def __init__(self, wav: WavFile, min_freq, max_freq, audio_filter: AudioFilter, return_func):
        super(FilterThread, self).__init__()
        self.wav = wav
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.audio_filter = audio_filter
        self.return_func = return_func

    def run(self):
        result = self.audio_filter.filter(min_freq=self.min_freq, max_freq=self.max_freq, wav=self.wav)
        self.return_func(result)
