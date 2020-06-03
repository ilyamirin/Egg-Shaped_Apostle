from werkzeug.datastructures import FileStorage
import wave
import deepspeech
import numpy as np

from core.stt_service import SttService
from core.utils import log_load

WEIGHTS_PATH = 'resources/deepspeech-weights.pbmm'
LM_PATH = 'resources/kenlm.scorer'

class DeepspeechSttService(SttService):
    _model: deepspeech.Model

    def __init__(self):
         self._model = log_load(lambda: deepspeech.Model(WEIGHTS_PATH), 'DeepSpeech model')
         log_load(lambda: self._model.enableExternalScorer(LM_PATH), 'KenLM language model')

    def transcribe(self, audio: FileStorage) -> str:
        with wave.open(audio, 'rb') as fin:
            features = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        
        return self._model.stt(features)
