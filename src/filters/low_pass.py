import struct
import wave
from os.path import join
from random import randint
from wave import Wave_read

from pandas import np
from scipy.signal import butter, filtfilt

import util, const

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


def filter_lowpassTest(wav: Wave_read, cutoff: int):
    signal = wav.readframes(-1)
    signal = np.fromstring(signal, "Int16")

    filtered: wave.Wave_write = wave.open(join(const.AUDIO_DIR, 'temp.wav'), 'w')
    filtered.setframerate(wav.getframerate())
    filtered.setsampwidth(wav.getsampwidth())
    filtered.setnchannels(wav.getnchannels())
    for frame in frames:
        data = struct.pack('<h', frame)
        filtered.writeframesraw(data)
    filtered.close()
    return wave.open(join(const.AUDIO_DIR, 'temp.wav'), 'r')


def filter_lowpass(wav: Wave_read, cutoff: int):
    signal = wav.data
    signal = np.fromstring(signal, "Int16")

    index = -1
    frames = []
    for frame in signal:
        index += 1
        if abs(frame) < cutoff:
            frames.append(10)
            pass
        else:
            frames.append(frame)

    wav.close()

    filtered: wave.Wave_write = wave.open(join(const.AUDIO_DIR, 'temp.wav'), 'w')
    filtered.setframerate(wav.getframerate())
    filtered.setsampwidth(wav.getsampwidth())
    filtered.setnchannels(wav.getnchannels())
    for frame in frames:
        data = struct.pack('<h', frame)
        filtered.writeframesraw(data)
    filtered.close()
    return wave.open(join(const.AUDIO_DIR, 'temp.wav'), 'r')

