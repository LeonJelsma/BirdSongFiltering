import threading


class FilterThread(threading.Thread):

    def __init__(self, data, filter_func, return_func):
        super(FilterThread, self).__init__()
        self.data = data
        self.filter_func = filter_func
        self.return_func = return_func

    def run(self):
        result = self.filter_func(self.data)
        self.return_func(result)
