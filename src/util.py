from os.path import join
from src import const
from scipy.io import wavfile

from src.wavfile import WavFile


def open_wav(name):
    rate, data = wavfile.read(join(const.AUDIO_DIR, name))
    return WavFile(name=name, rate=rate, data=data)


def write_wav(wav_file: WavFile):
    return wavfile.write(filename=join(const.OUTPUT_DIR, wav_file.name), rate=wav_file.rate, data=wav_file.data)


def get_ui_file(name: str):
    return join(const.UI_DIR, name)