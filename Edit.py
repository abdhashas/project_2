import librosa


# from Time_Stretch import stretch

def change_amplitude(signal, value):
    modified_audio = signal * value
    return modified_audio


def change_time_stretch(signal, value):
    modified_audio = librosa.effects.time_stretch(signal, rate=value)
    return modified_audio


def change_pitch_shift(signal, value, sample_rate):
    modified_audio = librosa.effects.pitch_shift(signal, sr=sample_rate, n_steps=value)
    return modified_audio
