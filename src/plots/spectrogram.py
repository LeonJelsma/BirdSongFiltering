from scipy import signal
import numpy as np
import pyqtgraph
from src.wavfile import WavFile


def get_spectrogram(wav: WavFile, graphics_layout: pyqtgraph.GraphicsLayoutWidget):
    f, t, Sxx = signal.spectrogram(wav.data, wav.rate)

    # Interpret image data as row-major instead of col-major
    pyqtgraph.setConfigOptions(imageAxisOrder='row-major')
    pyqtgraph.mkQApp()
    graphics_layout.clear()
    plot_widget = graphics_layout.addPlot()
    # A plot area (ViewBox + axes) for displaying the image

    # Item for displaying image data
    img = pyqtgraph.ImageItem()
    plot_widget.addItem(img)
    # Add a histogram with which to control the gradient of the image
    hist = pyqtgraph.HistogramLUTItem()
    # Link the histogram to the image
    hist.setImageItem(img)
    # If you don't add the histogram to the window, it stays invisible, but I find it useful.
    graphics_layout.addItem(hist)
    # Show the window
    graphics_layout.show()
    # Fit the min and max levels of the histogram to the data available
    hist.setLevels(np.min(Sxx), np.max(Sxx))
    # This gradient is roughly comparable to the gradient used by Matplotlib
    # You can adjust it and then save it using hist.gradient.saveState()
    hist.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(0.5, (0, 182, 188, 255)),
                   (1.0, (246, 111, 0, 255)),
                   (0.0, (75, 0, 113, 255))]})
    # Sxx contains the amplitude for each pixel
    img.setImage(Sxx)
    # Scale the X and Y Axis to time and frequency (standard is pixels)
    img.scale(t[-1] / np.size(Sxx, axis=1),
              f[-1] / np.size(Sxx, axis=0))
    # Limit panning/zooming to the spectrogram
    plot_widget.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
    # Add labels to the axis
    plot_widget.setLabel('bottom', "Time", units='s')
    # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
    plot_widget.setLabel('left', "Frequency", units='Hz')

    # Plotting with Matplotlib in comparison
    # plt.pcolormesh(t, f, Sxx)
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # plt.colorbar()
    # plt.show()

