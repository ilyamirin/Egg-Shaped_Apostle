#!/bin/python3

import numpy as np
import tensorflow as tf
# from timeit import default_timer as timer
from pydub import AudioSegment
import wave
from deepspeech import Model

# path to deepspeech model, originally in root of project/deepspeech
path_to_model = "/home/sde/Desktop/projects/Egg-Shaped_Apostle//deepspeech/models/"

# Path to the model (protocol buffer binary file)
model = path_to_model+"output_graph.pb"

# Path to the configuration file specifying the alphabet used by the network
alphabet = path_to_model+'alphabet.txt'

# path to the language model binary file
lm = 'lm.binary'

# Path to the language model trie file created with native_client/generate_trie
trie = 'trie'

#Default is selected based on the model's requirements
framerate = 16000

# You could process only n seconds.
crop_time = 900

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.50

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 2.10

# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training
# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

# Network Parameters
DEFAULT_SEED = 123


class DeepspeechRecognizer():
    def __init__(self):
        #self.model = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
        self.model = Model(model, BEAM_WIDTH)
        self.model.enableDecoderWithLM(alphabet, lm, trie, LM_WEIGHT, VALID_WORD_COUNT_WEIGHT)

    def recognize(self, audio_file):
        audio = AudioSegment.from_wav(audio_file)
        audio.set_frame_rate(16000)  # конвертация в 16кГц
        # audio = np.frombuffer(frames.readframes(frames.getnframes()), np.int16)
        # audio_length = len(audio) * (1 / framerate)
        # frames.close()
        result_sub = self.model.stt(audio, framerate)
        return result_sub

rcgnzr = DeepspeechRecognizer()
print(rcgnzr.recognize("test.wav"))

'''import tensorflow as tf
hello = tf.constant("Hello, world!")
session = tf.compat.v1.Session()
print(session.run(hello))

import tensorflow as tf
with tf.device('/gpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)

with tf.compat.v1.Session() as sess:
    print (sess.run(c))'''
