class AudioFilter:
    def __init__(self, filter_func):
        self.filter_func = filter_func

    def filter(self, data):
        return self.filter_func(data)
