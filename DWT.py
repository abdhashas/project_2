import numpy as np 
import pywt


def dwt(signal, wavelet='db4', levels=5):
    signal = signal.astype(np.float32)
    normalized_signal = signal / np.max(np.abs(signal)) 
    coeffs = pywt.wavedec(normalized_signal, wavelet, level=levels)
    reconstructed_signal = pywt.waverec(coeffs, wavelet)
    return reconstructed_signal 