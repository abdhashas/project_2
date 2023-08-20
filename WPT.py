import numpy as np
import pywt


def wpt(signal, wavelet='db4', levels=5):
    normalized_signal = signal / np.max(np.abs(signal))
    wp = pywt.WaveletPacket(normalized_signal, wavelet, 'symmetric', maxlevel=levels)
    wpt_coefficients = [node.data for node in wp.get_level(levels, 'freq')]
    reconstructed_signal = np.zeros(len(normalized_signal))
    leaves = wp.get_leaf_nodes()
    for i, coefficients in enumerate(wpt_coefficients):
        node_index = len(leaves) - 2 * i - 1
        node_path = leaves[node_index].path
        wp[node_path].data = coefficients
    reconstructed_signal = wp.reconstruct(update=True)
    return reconstructed_signal
