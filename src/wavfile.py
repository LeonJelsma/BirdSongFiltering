

class WavFile:
    def __init__(self, name, rate, data):
        self.name = name
        self.rate = rate
        self.frames = len(data)
        self.data = data
