import librosa
import scipy
from numpy import abs, max


class Audio:
    def __init__(self, samples, *, window_length, overlap, sample_rate):
        self.samples = samples
        self.fft_length = window_length
        self.window_length = window_length
        self.overlap = overlap
        self.sample_rate = sample_rate
        self.window = scipy.signal.hamming(self.window_length, sym=False)
        self.stft_features = librosa.stft(self.samples,
                                          n_fft=self.fft_length,
                                          win_length=self.window_length,
                                          hop_length=self.overlap,
                                          window=self.window, center=True)

    def get_dB_features(self):
        return librosa.amplitude_to_db(abs(self.stft_features), ref=max)

    def get_audio_from_stft_spectrogram(self):
        return librosa.istft(self.stft_features,
                             win_length=self.window_length,
                             hop_length=self.overlap,
                             window=self.window,
                             center=True)

    def save(self, name):
        librosa.output.write_wav(name, self.get_audio_from_stft_spectrogram(), sr=self.sample_rate)

