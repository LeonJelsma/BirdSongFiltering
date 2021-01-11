import numpy as np


def FFT_vectorized(x):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    x = checkIfPowTwo(x)
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :int(X.shape[1] / 2)]
        X_odd = X[:, int(X.shape[1] / 2):]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()


def checkIfPowTwo(DATA):
    # Check if the length of data corresponds to a 2**n number:
    POWER_2 = [2 ** x for x in range(50)]  # Create an array with 50 2**n values
    # print(POWER_2)
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
    DATA = np.append(DATA, [0 for x in range(
        DATAPOINTS_NEEDED)])  # Add the correct amount of datapoints to the DATA ndarray to form an 2**n array
    return np.array(DATA)
