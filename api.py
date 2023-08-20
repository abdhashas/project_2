from flask import Flask, request, send_file, jsonify,json
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import librosa
import pywt
import soundfile as sf
from scipy.io.wavfile import read, write
from DWT import dwt
from WPT import wpt
from LPC import lpc
import Edit 
app = Flask(__name__)
api = Api(app)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './saved'
ALLOWED_EXTENSIONS = 'wav'  # Define allowed audio file extensions
arr_reconstructed_signal=[]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET'])
# def hello():
#     return 'hello there'

@app.route('/dwt', methods=['POST'])
def perform_dwt():
    global arr_reconstructed_signal
    # data = request.json
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
        filepath = os.path.join('saved', filename+'.wav')
        audio_file.save(filepath)
        sample_rate, signal = read(filepath)

        # DWT
        reconstructed_signal = dwt(signal)#, wavelet, levels
    if amplitude != 1 :
        reconstructed_signal =Edit.change_amplitude(reconstructed_signal,amplitude)
    if time_stretch != 1 :
        reconstructed_signal =Edit.change_time_stretch(reconstructed_signal,time_stretch)
    if pitch_shift != 1 : 
        reconstructed_signal =Edit.change_pitch_shift(reconstructed_signal,pitch_shift,sample_rate)
    arr_reconstructed_signal = reconstructed_signal
    output_filename =filename+" dwt.wav"
    # output_filename = output_filename / np.max(np.abs(output_filename))
    wavfile.write(output_filename, sample_rate, reconstructed_signal) 

    return send_file(output_filename, as_attachment=True)


@app.route('/wpt', methods=['POST'])
def perform_wpt():
    # data = request.json
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
        filepath = os.path.join('saved', filename+'.wav')
        audio_file.save(filepath)
        sample_rate, signal = read(filepath)

        # wpt
        reconstructed_signal = wpt(signal)#, wavelet, levels
    if amplitude != 1 :
        reconstructed_signal =Edit.change_amplitude(reconstructed_signal,amplitude)
    if time_stretch != 1 :
        reconstructed_signal =Edit.change_time_stretch(reconstructed_signal,time_stretch)
    if pitch_shift != 1 : 
        reconstructed_signal =Edit.change_pitch_shift(reconstructed_signal,pitch_shift,sample_rate)
 
    output_filename = filename+" wpt.wav"
    # output_filename = output_filename / np.max(np.abs(output_filename))
    wavfile.write(output_filename, sample_rate, reconstructed_signal) 


    return send_file(output_filename, as_attachment=True)

@app.route('/lpc', methods=['POST'])
def perform_lpc():
    # data = request.json
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
        filepath = os.path.join('saved', filename+'.wav')
        audio_file.save(filepath)
        sample_rate, signal = read(filepath)

        # lpc
        reconstructed_signal = lpc(signal)#, wavelet, levels
    if amplitude != 1 :
        reconstructed_signal =Edit.change_amplitude(reconstructed_signal,amplitude)
    if time_stretch != 1 :
        reconstructed_signal =Edit.change_time_stretch(reconstructed_signal,time_stretch)
    if pitch_shift != 1 : 
        reconstructed_signal =Edit.change_pitch_shift(reconstructed_signal,pitch_shift,sample_rate)
    filename = secure_filename(audio_file.filename)
    output_filename = filename+" lpc.wav"
    # output_filename = output_filename / np.max(np.abs(output_filename))
    wavfile.write(output_filename, sample_rate, reconstructed_signal) 


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
        filepath = os.path.join('saved', filename+'.wav')
        audio_file.save(filepath)
        audio_data, sample_rate = sf.read(filepath)
        if len(audio_data.shape) > 1:
            audio_array = audio_data.T
        else:
            audio_array = np.array([audio_data])

        arr_reconstructed_signal=audio_array
 
        return send_file(filepath, as_attachment=True)
    else:
        return 'Invalid audio file'


@app.route('/download/<filename>', methods=['GET'])
def download_audio(filename):
    global arr_reconstructed_signal
    filepath = os.path.join('saved', filename+'.wav')
    audio_data, sample_rate = sf.read(filepath)
    if len(audio_data.shape) > 1:
        audio_array = audio_data.T
    else:
        audio_array = np.array([audio_data])

    arr_reconstructed_signal=audio_array
    return send_file(filepath, as_attachment=True)


@app.route('/download/<filename>/array', methods=['GET'])
def download_sond_orginal(filename):
    global arr_reconstructed_signal
    array= arr_reconstructed_signal
    arr_reconstructed_signal=[]
    return { 'reconstructed_signal': [reconstructed_signal1.tolist() for reconstructed_signal1 in array]}


if __name__ == '__main__':
    app.run(debug=True)

# host='192.168.1.3'
