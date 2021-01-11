import numpy as np
from matplotlib.figure import Figure


def get_raw_audio_graph(title):
    figure = Figure()
    figure.suptitle(title)
    return figure


def plot_raw_audio(wav, figure, title, color):
    # Extract Raw Audio from Wav File
    signal = wav.data
    signal = np.fromstring(signal, "Int16")
    fs = wav.rate

    # If Stereo
    # if wav.getnchannels() == 2:
    #    print("Just mono files")
    #    sys.exit(0)

    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    figure = Figure()
    plot = figure.add_subplot(111)
    figure.suptitle(title)
    plot.plot(Time, signal, 'C1', label='C1')
    # self.auto_range_unfiltered()
    plot.show()
    # plt.figure(1)
    # plt.title(title)
    # plt.plot(Time, signal)
    return figure
