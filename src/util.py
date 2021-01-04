from pydub import AudioSegment


def decode_mp3(file):
    sound = AudioSegment.from_mp3(file=file)

    # get raw audio data as a bytestring
    raw_data = sound.raw_data
    # get the frame rate
    sample_rate = sound.frame_rate
    # get amount of bytes contained in one sample
    sample_size = sound.sample_width
    # get channels
    channels = sound.channels
