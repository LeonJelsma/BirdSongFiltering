import threading

from src.filters.audiofilter import AudioFilter


class FilterThread(threading.Thread):

    def __init__(self, data, audio_filter: AudioFilter, return_func):
        super(FilterThread, self).__init__()
        self.data = data
        self.audio_filter = audio_filter
        self.return_func = return_func

    def run(self):
        result = self.audio_filter.filter(self.data)
        self.return_func(result)
