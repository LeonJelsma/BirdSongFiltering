import os
from os.path import join

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES = join(join(SRC_DIR, ".."), "resources")
ASSET_DIR = join(RESOURCES, "assets")
UI_DIR = join(RESOURCES, "ui")
VIEWS_DIR = join(UI_DIR, "views")
STYLES_DIR = join(UI_DIR, "styles")
AUDIO_DIR = join(join(SRC_DIR, ".."), "audio")
OUTPUT_DIR = join(join(SRC_DIR, ".."), "output")
PLOT_OUTPUT_DIR = join(OUTPUT_DIR, "plots")
LABELED_BIRD_SOUNDS_DIR = join(AUDIO_DIR, "labeled")
