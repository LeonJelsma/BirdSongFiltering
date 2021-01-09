import Butterworth
from numpy import exp, pi, int16, array, append
from scipy.io import wavfile

BOTTOM_FREQUENCY = 6000
TOP_FREQUENCY    = 8000

FILE_NAMES = {
    "Processed" : "test_single.wav", # Processed filename [.wav]
    "Raw_T/F"   : True, # (False) False = Use processed filename only, True = Use Raw filename first, then Processed filename
    "Raw"       : "audio/single_mono.wav", # (None) Unprocessed filename [.wav]
}

TEXT_FILE = {
    "TXTFILE": True, # (False) Use true if you want to create a txt file
    "TXTFILENAME": "FFT.txt", # (None) Name of the txt file you want to create
}

class FFT():
    """
    FFT Class functions:
        Filter(B_FREQ, T_FREQ, AUDIO_FILE=None, RAW=[False, None]):
            B_FREQ: The bottom frequency of the bandpass filter
            T_FREQ: The top frequency of the bandpass filter
            AUDIO_FILE: Path name of the processed audio file (.wav file)
            
            OPTIONAL ARGS:
                RAW:
                    RAW[0]: (True/False) Select True if the .wavfile is unprocessed [Standard value = False]
                    RAW[1]: File location of the 'raw' .wav file
                    If RAW[0] is set to True, use the AUDIO_FILE argument as the newly created processed file location.
                
                CREATE_FFT_TXT_FILE:
                    CREATE_FFT_TXT_FILE[0]: Set True if the FFT function should be put into a .txt file [Standard value = False]
                    CREATE_FFT_TXT_FILE[1]: Desired file name
    """

    def FFT_Function(self, B_FREQ, T_FREQ, AUDIO_FILE=None, RAW=[False, None], CREATE_FFT_TXT_FILE=[False, None]):
        BANDPASS = [B_FREQ, T_FREQ]
        # If the first value of the RAW array is set to True
        if RAW[0] != False:
            SAMPLE_FREQUENCY, DATA = FFT().readFile(RAW[1]) # Read 'RAW' .wav file
            appliedFilter = array(FFT().bandpassFilter(DATA, B_FREQ=BANDPASS[0], T_FREQ=BANDPASS[1], S_FREQ=SAMPLE_FREQUENCY))
            FFT().writeFile(appliedFilter, OUTPUT_NAME=AUDIO_FILE, SAMPLE_FREQUENCY=SAMPLE_FREQUENCY)

        SAMPLE_FREQUENCY, DATA = FFT().readFile(AUDIO_FILE) # Read processed audio file
        NEW_DATA = FFT().checkIfPowTwo(DATA) # Check if len(DATA) == 2**n, otherwise make len(DATA) == 2**n
        FFT_DATA = FFT().fastFourierTransform(NEW_DATA) # Use the FFT algorithm to create Fourier Transform data

        if CREATE_FFT_TXT_FILE != False:
            FFT().create_txt_file(FFT_DATA, CREATE_FFT_TXT_FILE[1])
        
        return FFT_DATA
    
    def create_txt_file(self, FFT_DATA, TXT_FILE_NAME):
        txt_file = open(TXT_FILE_NAME, 'w')
        new_array = []
        for x in FFT_DATA:
            new_array.append(x)
        
        txt_file.write(f"{new_array}") #Write all datapoints into a text file
        txt_file.close()
        print(f"Fast Fourier Transform succesfully saved as: {TXT_FILE_NAME}")

    def checkIfPowTwo(self, DATA):
        # Check if the length of data corresponds to a 2**n number:
        POWER_2 = [2**x for x in range(50)] # Create an array with 50 2**n values
        # print(POWER_2)
        POWER_2_DATA = 0
        count = 0
        for x in POWER_2: # Run a for loop through the power of 2 array
            if x >= len(DATA): # If the power of 2 value is larger than the length of the numpy ndarray (sound data)
                if count == 0: # Check if this is the first time that the value is larger than len(DATA)
                    # print(x)
                    POWER_2_DATA = x # Set the value of 2**n
                    count = 1 # Set the count to 1 so the next number of 2**n doesn't overwrite the correct number
                else: # If the count is not equal to 0
                    pass
            else: # If 2**n is not larger than len(DATA)
                pass

        DATAPOINTS_NEEDED = POWER_2_DATA - len(DATA) # Subtract the len(DATA) from POWER_2_DATA
        DATA = append(DATA, [0 for x in range(DATAPOINTS_NEEDED)]) # Add the correct amount of datapoints to the DATA ndarray to form an 2**n array
        return array(DATA)

    def bandpassFilter(self, DATA, B_FREQ=None, T_FREQ=None, S_FREQ=None):
        # Create bandwidth with the Butterworth filter
        butterworth = Butterworth.ButterworthFilter(B_FREQ=B_FREQ, T_FREQ=T_FREQ)
        bandpass = butterworth.bandpass(S_FREQ=S_FREQ)
        # Apply generated values from the Butterworth filter to the audio dataset
        appliedFilter = Butterworth.applyFilter(DATA=DATA, XY_Values=bandpass)
        return appliedFilter
        
    def writeFile(self, APPLIED_FILTER, OUTPUT_NAME=None, SAMPLE_FREQUENCY=None):
        wavfile.write(OUTPUT_NAME, SAMPLE_FREQUENCY, APPLIED_FILTER.astype(int16))

    def readFile(self, FILE_NAME):
        SAMPLE_FREQUENCY, DATA = wavfile.read(FILE_NAME)
        return SAMPLE_FREQUENCY, DATA

    def fastFourierTransform(self, vector): # Fast Fourier Transform function
        n = len(vector) # Length of the numpy ndarray
        if n <= 1:  # Base case
            return vector
        elif n % 2 != 0: # Check if the length of the numpy ndarray is equal to a 2**n
            raise ValueError("Length is not a power of 2")
        else:
            k = n // 2
            even = FFT().fastFourierTransform(vector[0 : : 2])
            odd  = FFT().fastFourierTransform(vector[1 : : 2])
            return [even[i % k] + odd[i % k] * exp(i * -2j * pi / n) for i in range(n)]

def main():
    FFT_VALUE = FFT().FFT_Function(
        BOTTOM_FREQUENCY,
        TOP_FREQUENCY,
        AUDIO_FILE=FILE_NAMES["Processed"],
        RAW=(
            FILE_NAMES["Raw_T/F"],
            FILE_NAMES["Raw"]
            ),
        CREATE_FFT_TXT_FILE=(
            TEXT_FILE["TXTFILE"],
            TEXT_FILE["TXTFILENAME"]
        )
    )

if __name__ == "__main__":
    main()