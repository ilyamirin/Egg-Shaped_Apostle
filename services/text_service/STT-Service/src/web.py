import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from core.deepspeech_stt_service import DeepspeechSttService
import wave


ds_stt_service = DeepspeechSttService()


print('Starting web server...', flush=True)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return {
        'service': 'stt-service',
        'status': 'OK'
    }

@app.route('/transcribe', methods=['POST'])
def transcript():
    if 'audio' not in request.files or request.files['audio'].filename == '':
        return { 'type': 'BadRequestException', 'message': 'No file provided' }, 400

    file_ = request.files['audio']

    try:
        result = ds_stt_service.transcribe(file_)
    except Exception as e:
        traceback.print_exc()
        return { 'type': str(type(e).__name__), 'message': str(e) }, 500

    return { 'result': result }

app.run(host='0.0.0.0')
