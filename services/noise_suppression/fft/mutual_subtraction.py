from matplotlib import pyplot as plt

import numpy as np

import librosa
from librosa import display

from synchronization import synchronize
from audio import Audio


def draw_spectrogram(name, dB_features, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(dB_features, sr=sr, y_axis='log', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('stft spectrogram')
    plt.tight_layout()
    plt.savefig(name)


def mutual_substraction(file_1, file_2, treshold=1.8, draw=False):
    samples_1, samples_2, sr, delay = synchronize(file_1, file_2)
    audio_1 = Audio(samples_1, window_length=1024, overlap=128, sample_rate=sr)
    audio_2 = Audio(samples_2, window_length=1024, overlap=128, sample_rate=sr)
    if draw:
        draw_spectrogram(file_1 + '_spec.png', audio_1.get_dB_features(), sr)
        draw_spectrogram(file_2 + '_spec.png', audio_2.get_dB_features(), sr)
    audio_1.stft_features[np.abs(audio_1.stft_features - audio_2.stft_features) < treshold] = 0
    audio_2.stft_features[np.abs(audio_2.stft_features - audio_1.stft_features) < treshold] = 0
    if draw:
        draw_spectrogram(file_1 + '_clean_spec.png', audio_1.get_dB_features(), sr)
        draw_spectrogram(file_2 + '_clean_spec.png', audio_2.get_dB_features(), sr)
    return audio_1.get_audio_from_stft_spectrogram(), audio_2.get_audio_from_stft_spectrogram()
    #audio_1.save(file_1 + '_clean.wav')
    #audio_2.save(file_2 + '_clean.wav')


# file_1, file_2 = '0_2_0_2020-06-21T17:38:05.824776.wav', '0_3_0_2020-06-21T17:38:05.824797.wav'
# mutual_substraction(file_1, file_2, draw=True)
