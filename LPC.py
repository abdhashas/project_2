import librosa
import numpy as np
from scipy.signal import lfilter


def lpc(signal):
    A = librosa.lpc(signal, order=6)
    B = np.hstack([[0], -1 * A[1:]])
    y_hat = lfilter(B, [1], signal)
    return y_hat
