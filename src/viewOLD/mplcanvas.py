from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.plots import frequencies
from src.wavfile import WavFile


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, wav_file: WavFile = None):
        fig = frequencies.plot_spectogram(wav_file, title=wav_file.name)
        super(MplCanvas, self).__init__(fig)
