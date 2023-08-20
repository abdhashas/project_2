def generate_multipart(audio_bytes, audio_array, sample_rate):
    # مولد الأجزاء متعددة الوسائط
    boundary = 'frame'
    yield f'--{boundary}\r\n'
    yield f'Content-Type: audio/wav\r\n\r\n'
    yield audio_bytes
    yield f'\r\n--{boundary}\r\n'
    yield f'Content-Type: application/json\r\n\r\n'
    yield f'{{"sample_rate": {sample_rate}, "audio_array": {audio_array.tolist()}}}'
    yield f'\r\n--{boundary}--\r\n'
