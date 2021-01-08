from src.filters.audiofilter import AudioFilter


def test_filter(x):
    y = [0] * len(x)
    for n in range(2, len(x)):
        y[n] = 0.1293 * x[n] - 0.1293 * x[n - 2] + 0.964 * y[n - 1] - 0.4551 * y[n - 2]
    return y


def get_test_filter():
    return AudioFilter(test_filter)