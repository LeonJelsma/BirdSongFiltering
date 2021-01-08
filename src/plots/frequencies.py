
import numpy as np
from matplotlib.figure import Figure
from wave import Wave_read

def plot_spectogram(wav, title):
    # Extract Raw Audio from Wav File
    signal = wav.data
    signal = np.fromstring(signal, "Int16")
    fs = wav.rate

    # If Stereo
    #if wav.getnchannels() == 2:
    #    print("Just mono files")
    #    sys.exit(0)


    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    figure = Figure()
    plot = figure.add_subplot(111)
    figure.suptitle(title)
    plot.plot(Time, signal)
    #plt.figure(1)
    #plt.title(title)
    #plt.plot(Time, signal)
    return figure
