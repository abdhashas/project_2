from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import numpy as np
import soundfile as sf
import librosa
from DWT import dwt
from WPT import wpt
from LPC import lpc
import Edit

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './saved'
ALLOWED_EXTENSIONS = 'wav'  # Define allowed audio file extensions
arr_reconstructed_signal = []


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET'])
# def hello():
#     return 'hello there'
def decode():
    global arr_reconstructed_signal
    amplitude = 1
    time_stretch = 1
    pitch_shift = 1
    if 'Amplitude' in request.form:
        amplitude = float(request.form['Amplitude'])
    if 'Time_stretch' in request.form:
        time_stretch = float(request.form['Time_stretch'])
    if 'Pitch_shift' in request.form:
        pitch_shift = float(request.form['Pitch_shift'])
    if 'audio' not in request.files:
        return 'No audio part'
    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'No selected file'

    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join('saved', filename)
        audio_file.save(filepath)
        signal, sample_rate = librosa.load(filepath, sr=44100)
    return signal, amplitude, time_stretch, pitch_shift, filename, sample_rate


def edit(signal, sample_rate, amplitude, time_stretch, pitch_shift):
    global arr_reconstructed_signal
    if amplitude != 1:
        signal = Edit.change_amplitude(signal, amplitude)
    if time_stretch != 1:
        signal = Edit.change_time_stretch(signal, time_stretch)
    if pitch_shift != 1:
        signal = Edit.change_pitch_shift(signal, pitch_shift, sample_rate)
    arr_reconstructed_signal = signal
    return signal


@app.route('/dwt', methods=['POST'])
def perform_dwt():
    global arr_reconstructed_signal
    signal, amplitude, time_stretch, pitch_shift, filename, sample_rate = decode()
    reconstructed_signal = dwt(signal)  # , wavelet, levels
    reconstructed_signal = edit(reconstructed_signal, sample_rate, amplitude, time_stretch, pitch_shift)
    output_filename = os.path.join('saved', 'dwt_' + filename)
    sf.write(output_filename, reconstructed_signal, int(sample_rate))

    return send_file(output_filename, as_attachment=True)


@app.route('/wpt', methods=['POST'])
def perform_wpt():
    signal, amplitude, time_stretch, pitch_shift, filename, sample_rate = decode()
    # wpt
    reconstructed_signal = wpt(signal)  # , wavelet, levels
    reconstructed_signal = edit(reconstructed_signal, sample_rate, amplitude, time_stretch, pitch_shift)
    output_filename = os.path.join('saved', 'wpt_' + filename)
    # output_filename = output_filename / np.max(np.abs(output_filename))
    sf.write(output_filename, reconstructed_signal, int(sample_rate))

    return send_file(output_filename, as_attachment=True)


@app.route('/lpc', methods=['POST'])
def perform_lpc():
    signal, amplitude, time_stretch, pitch_shift, filename, sample_rate = decode()
    reconstructed_signal = lpc(signal)
    reconstructed_signal = edit(reconstructed_signal, sample_rate, amplitude, time_stretch, pitch_shift)
    output_filename = os.path.join('saved', 'lpc_' + filename)
    sf.write(output_filename, reconstructed_signal, int(sample_rate))

    return send_file(output_filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_audio():
    global arr_reconstructed_signal
    if 'audio' not in request.files:
        return 'No audio part'

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'No selected file'

    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join('saved', filename)
        audio_file.save(filepath)
        audio_data, sample_rate = librosa.load(filepath, sr=44100)
        if len(audio_data.shape) > 1:
            audio_array = audio_data.T
        else:
            audio_array = np.array([audio_data])

        arr_reconstructed_signal = audio_array

        return send_file(filepath, as_attachment=True)
    else:
        return 'Invalid audio file'


@app.route('/download/<filename>', methods=['GET'])
def download_audio(filename):
    global arr_reconstructed_signal
    filepath = os.path.join('saved', filename)
    audio_data, sample_rate = librosa.load(filepath, sr=44100)
    if len(audio_data.shape) > 1:
        audio_array = audio_data.T
    else:
        audio_array = np.array([audio_data])

    arr_reconstructed_signal = audio_array
    return send_file(filepath, as_attachment=True)


@app.route('/array/<filename>', methods=['GET'])
def download_sound_original(filename):
    path = f'saved/{str(filename)}'
    if os.path.exists(path):
        signal, _ = librosa.load(path)
        return {'array': signal.tolist()}
    else:
        return 'file does not exist'


if __name__ == '__main__':
    app.run(debug=True)

# host='192.168.1.3'


# @app.route('/array/<filename>', methods=['GET'])
# def download_sound_original(filename):
#     global arr_reconstructed_signal
#     array = arr_reconstructed_signal
#     arr_reconstructed_signal = []
#     return {'array': array.tolist()}
