from scipy.io import wavfile
from scipy import signal
import numpy as np


def filter2(x):
    y = [0]*len(x)
    for n in range(2, len(x)):
        y[n] = x[n] - x[n-1] - 0.2217*x[n-1] + 0.2217*x[n-2] + 0.2217*y[n-1]
    return y


def filter3(x):
    y = [0]*len(x)
    for n in range(2, len(x)):
        y[n] = 0.1293*x[n] - 0.1293*x[n-2] + 0.964*y[n-1] - 0.4551*y[n-2]
    return y


sr, x = wavfile.read('single_mono.wav')
y = x

#b = signal.firwin(101, cutoff=1500, fs=sr, pass_zero=False)

#y = signal.lfilter(b, [1.0], y)

y = np.array(filter3(y))

wavfile.write('test1.wav', sr, y.astype(np.int16))
