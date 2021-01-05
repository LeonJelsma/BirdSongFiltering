import os
from os.path import join

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = join(SRC_DIR, "ui")
AUDIO_DIR = join(join(SRC_DIR, ".."), "audio")
OUTPUT_DIR = join(join(SRC_DIR, ".."), "output")
PLOT_OUTPUT_DIR = join(OUTPUT_DIR, "plots")