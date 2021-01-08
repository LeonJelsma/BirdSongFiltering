from collections import Iterable


class WavFile:
    def __init__(self, name, rate, data):
        self.name = name
        self.rate = rate
        self.frames = len(data)
        self.data = data
        if isinstance(data[0], Iterable):
            self.channels = len(data[0])
        else:
            self.channels = 1
