from src.Butterworth import AUDIO_FILE_LOCATION, ButterworthFilter, OUTPUT_NAME
from numpy import exp, sqrt, pi, int16, array
from scipy.io import wavfile

from src.wavfile import WavFile

BOTTOM_FREQUENCY = 6000
TOP_FREQUENCY = 8000
# AUDIO_FILE_LOCATION = 'audio/single_mono.wav'
AUDIO_FILE_LOCATION = 'test1.wav'
OUTPUT_NAME = 'test1.wav'


class ButterworthFilter():
    def __init__(self, B_FREQ=None, T_FREQ=None):
        self.W_Bottom = 2 * pi * B_FREQ  # Radians of BOTTOM_FREQUENCY
        self.W_Top = 2 * pi * T_FREQ  # Radians of TOP_FREQUENCY
        self.W_Zero = sqrt(self.W_Bottom * self.W_Top)  # Square root of W_One*W_Two
        self.bandwidth = self.W_Top - self.W_Bottom  # Total bandwidth of the bandpass filter
        self.Qc = self.W_Zero / self.bandwidth

    def bandpass(self, S_FREQ=None):
        SAMPLE = 2 * S_FREQ
        A_Val = ((self.W_Zero ** 2) / (self.Qc ** 2)) * SAMPLE ** 2  # Value of A
        B_Val = SAMPLE ** 4  # Value of B
        C_Val = ((sqrt(2) * self.W_Zero) / self.Qc) * SAMPLE ** 3  # Value of C
        D_Val = (2 * self.W_Zero ** 2 + (self.W_Zero ** 2) / (self.Qc ** 2)) * SAMPLE ** 2  # Value of D
        E_Val = ((sqrt(2) * self.W_Zero ** 3) / self.Qc) * SAMPLE  # Value of E
        F_Val = self.W_Zero ** 4  # Value of F

        BCDEF = (B_Val + C_Val + D_Val + E_Val + F_Val)

        Xn_4 = A_Val / BCDEF  # Value of X[n-4]
        Xn_2 = -((2 * A_Val) / BCDEF)  # Value of X[n-2]
        Xn = A_Val / BCDEF  # Value of X[n]
        Yn_4 = -(B_Val - C_Val + D_Val - E_Val + F_Val) / BCDEF  # Value of Y[n-4]
        Yn_3 = -(-4 * B_Val + 2 * C_Val - 2 * E_Val + 4 * F_Val) / BCDEF  # Value of Y[n-3]
        Yn_2 = -(6 * B_Val - 2 * D_Val + 6 * F_Val) / BCDEF  # Value of Y[n-2]
        Yn_1 = -(-4 * B_Val - 2 * C_Val + 2 * E_Val + 4 * F_Val) / BCDEF  # Value of Y[n-1]

        print(
            f"Y[n] = {Xn_4}X[n-4] + {Xn_2}X[n-2] + {Xn}X[n] + {Yn_4}Y[n-4] + {Yn_3}Y[n-3] + {Yn_2}Y[n-2] + {Yn_1}Y[n-1]")
        bandpass = [Xn_4, Xn_2, Xn, Yn_4, Yn_3, Yn_2, Yn_1]
        return bandpass


def apply_filter(DATA=None, XY_Values=None):
    Y = [0] * len(DATA)
    for n in range(2, len(DATA)):
        Y[n] = XY_Values[0] * DATA[n - 4] + XY_Values[1] * DATA[n - 2] + XY_Values[2] * DATA[n] + XY_Values[3] * Y[
            n - 4] + XY_Values[4] * Y[n - 3] + XY_Values[5] * Y[n - 2] + XY_Values[6] * Y[n - 1]
    return Y


import cmath


def transform_radix2(vector):  # Fast Fourier Transform function
    n = len(vector)  # Length of the numpy ndarray
    if n <= 1:  # Base case
        return vector
    elif n % 2 != 0:  # Check if the length of the numpy ndarray is equal to a 2**n
        raise ValueError("Length is not a power of 2")
    else:
        k = n // 2
        even = transform_radix2(vector[0:: 2])
        odd = transform_radix2(vector[1:: 2])
        return [even[i % k] + odd[i % k] * cmath.exp(i * -2j * cmath.pi / n) for i in range(n)]


def main():
    SAMPLE_FREQUENCY, DATA = wavfile.read(AUDIO_FILE_LOCATION)

    # Check if the length of data corresponds to a 2**n number:
    POWER_2 = [2 ** x for x in range(50)]  # Create an array with 50 2**n values
    # print(POWER_2)

    import numpy
    POWER_2_DATA = 0
    count = 0
    for x in POWER_2:  # Run a for loop through the power of 2 array
        if x >= len(DATA):  # If the power of 2 value is larger than the length of the numpy ndarray (sound data)
            if count == 0:  # Check if this is the first time that the value is larger than len(DATA)
                # print(x)
                POWER_2_DATA = x  # Set the value of 2**n
                count = 1  # Set the count to 1 so the next number of 2**n doesn't overwrite the correct number
            else:  # If the count is not equal to 0
                pass
        else:  # If 2**n is not larger than len(DATA)
            pass

    DATAPOINTS_NEEDED = POWER_2_DATA - len(DATA)  # Subtract the len(DATA) from POWER_2_DATA
    DATA = numpy.append(DATA, [0 for x in range(
        DATAPOINTS_NEEDED)])  # Add the correct amount of datapoints to the DATA ndarray to form an 2**n array
    print(len(DATA))

    ret_val = transform_radix2(DATA)
    print(ret_val)
    txt_file = open("OUTPUT.txt", 'w')
    new_array = []
    for x in ret_val:
        new_array.append(x)
    
    txt_file.write(f"{new_array}") #Write all datapoints into a text file
    txt_file.close()


def filter_wav(wav: WavFile, min_freq, max_freq):
    sample_freq = wav.rate
    bandpass = ButterworthFilter(B_FREQ=min_freq, T_FREQ=max_freq).bandpass(S_FREQ=sample_freq)
    applied_filter = array(apply_filter(DATA=wav.data, XY_Values=bandpass))
    wav.data = applied_filter.astype(int16)
    return wav


if __name__ == "__main__":
    main()
