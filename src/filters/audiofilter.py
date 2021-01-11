from wavfile import WavFile


class AudioFilter:
    def __init__(self, filter_func):
        self.filter_func = filter_func

    def filter(self, wav: WavFile, min_freq, max_freq):
        return self.filter_func(wav, min_freq, max_freq)
