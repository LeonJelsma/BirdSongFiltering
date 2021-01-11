import os
from os.path import join
import const
from scipy.io import wavfile

from wavfile import WavFile


def open_wav(path):
    rate, data = wavfile.read(os.path.normpath(path))
    return WavFile(name=os.path.basename(os.path.normpath(path)), rate=rate, data=data)


def write_wav(wav_file: WavFile):
    return wavfile.write(filename=join(const.OUTPUT_DIR, wav_file.name), rate=wav_file.rate, data=wav_file.data)


def get_ui_file(name: str):
    return join(const.VIEWS_DIR, name)


def get_style(name: str):
    return join(const.STYLES_DIR, name)


def get_asset(name: str):
    return join(const.ASSET_DIR, name)
