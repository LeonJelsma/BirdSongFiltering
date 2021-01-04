from os.path import join
import os
from src import const
import wave


def open_wav(name):
    return wave.open(join(const.AUDIO_DIR, name), "r")