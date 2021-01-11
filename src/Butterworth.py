from numpy import pi, sqrt, array, int16

# BOTTOM_FREQUENCY = 2000
# TOP_FREQUENCY = 10000
# AUDIO_FILE_LOCATION = 'audio/multiple_mono.wav'
# OUTPUT_NAME = 'test1.wav'

class ButterworthFilter():
    def __init__(self, B_FREQ=None, T_FREQ=None):
        self.W_Bottom = 2 * pi * B_FREQ                 # Radians of BOTTOM_FREQUENCY
        self.W_Top = 2 * pi * T_FREQ                    # Radians of TOP_FREQUENCY
        self.W_Zero = sqrt(self.W_Bottom * self.W_Top)  # Square root of W_One*W_Two
        self.bandwidth = self.W_Top - self.W_Bottom     # Total bandwidth of the bandpass filter
        self.Qc = self.W_Zero/self.bandwidth
    
    def bandpass(self, S_FREQ=None, test=False):
        SAMPLE = 2*S_FREQ
        A_Val = ((self.W_Zero**2)/(self.Qc**2))*SAMPLE**2                   # Value of A
        B_Val = SAMPLE**4                                                   # Value of B
        C_Val = ((sqrt(2)*self.W_Zero)/self.Qc)*SAMPLE**3                   # Value of C
        D_Val = (2*self.W_Zero**2+(self.W_Zero**2)/(self.Qc**2))*SAMPLE**2  # Value of D
        E_Val = ((sqrt(2)*self.W_Zero**3)/self.Qc)*SAMPLE                   # Value of E
        F_Val = self.W_Zero**4                                              # Value of F

        BCDEF = (B_Val+C_Val+D_Val+E_Val+F_Val)

        Xn_4 = A_Val/BCDEF                               # Value of X[n-4]
        Xn_2 = -((2*A_Val)/BCDEF)                        # Value of X[n-2]
        Xn   = A_Val/BCDEF                               # Value of X[n]
        Yn_4 = -(B_Val-C_Val+D_Val-E_Val+F_Val)/BCDEF    # Value of Y[n-4]
        Yn_3 = -(-4*B_Val+2*C_Val-2*E_Val+4*F_Val)/BCDEF # Value of Y[n-3]
        Yn_2 = -(6*B_Val-2*D_Val+6*F_Val)/BCDEF          # Value of Y[n-2]
        Yn_1 = -(-4*B_Val-2*C_Val+2*E_Val+4*F_Val)/BCDEF # Value of Y[n-1]

        if test == True: # For testing only
            #print(f"Y[n] = {Xn_4}X[n-4] + {Xn_2}X[n-2] + {Xn}X[n] + {Yn_4}Y[n-4] + {Yn_3}Y[n-3] + {Yn_2}Y[n-2] + {Yn_1}Y[n-1]")
            pass
        bandpass = [Xn_4, Xn_2, Xn, Yn_4, Yn_3, Yn_2, Yn_1]
        return bandpass

def applyFilter(DATA=None, XY_Values=None):
    Y = [0]*len(DATA)
    for n in range(2, len(DATA)):
        Y[n] = XY_Values[0]*DATA[n-4] + XY_Values[1]*DATA[n-2] + XY_Values[2]*DATA[n] + XY_Values[3]*Y[n-4] + XY_Values[4]*Y[n-3] + XY_Values[5]*Y[n-2] + XY_Values[6]*Y[n-1]
    return Y