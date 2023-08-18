from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './saved'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}  # Define allowed audio file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return 'No audio part'

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'No selected file'

    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        return 'Audio uploaded successfully'
    else:
        return 'Invalid audio file'


@app.route('/download/<filename>', methods=['GET'])
def download_audio(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
