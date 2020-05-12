import librosa
from matplotlib import pyplot as plt
import numpy as np
import scipy
from librosa import display
import datetime

file_1, file_2 = '2_2_0_2020-03-24T17_35_33.087154.wav', '2_1_0_2020-03-24T17_35_33.077595.wav'
format = '%Y-%m-%dT%H_%M_%S.%f'

def get_timestamp(filename):
    timestamp = filename[6:-4]
    return datetime.datetime.strptime(timestamp, format)

def sort_start_time(file_1, file_2):

get_timestamp(file_1)
# samples1, sampling_rate1 = librosa.load('Untitled 1.wav')
# samples2, sampling_rate2 = librosa.load('Untitled 2.wav')

#
# time1 = 0.077595
# time2 = 0.087154
# delay = time2 - time1
# delay_samples = int(sampling_rate2*delay)
#
#
# def get_sync_delay():
#     eps_t = 1
#     slice_size = int(sampling_rate1 * eps_t)
#     slice1 = samples1[:slice_size]
#     slice2 = samples2[:slice_size]
#
#     # сравнение двух аудио по абсолютной разнице
#     MSE_list = []
#     for i in range(slice_size)[1:slice_size//2]:
#         slice1_temp = slice1[i:]
#         slice2_temp = slice2[:-i]
#         MSE_list.append(np.mean((np.abs(slice1_temp) - np.abs(slice2_temp))**2))
#     return np.argmin(MSE_list)
#
# samples1 = samples1[get_sync_delay():]
#
# librosa.output.write_wav('synchronized untitled1.wav', samples1, sampling_rate1)
#
# def fft_plot(audio, sampling_rate):
#     plt.figure()
#     n = len(audio)
#     T = 1/sampling_rate
#     yf = scipy.fft(audio)
#     xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
#     fig, ax = plt.subplots()
#     ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
#     plt.grid()
#     plt.xlabel('freq ->')
#     plt.ylabel('magnitude')
#     plt.savefig('fig2.png')


#
# fft_plot(samples, sampling_rate)
#
# def spectrogram(samples,
#                 sample_rate,
#                 stride_ms=10.0,
#                 window_ms=20.0,
#                 max_freq=None,
#                 eps=1e-14):
#     stride_size = int(1e-3 * sample_rate * stride_ms)
#     window_size = int(1e-3 * sample_rate * window_ms)
#
#     # extract strided windows
#     truncate_size = (len(samples) - window_size) % stride_size
#     samples = samples[:len(samples) - truncate_size]
#     nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
#     nstrides = (samples.strides[0], samples.strides[0] * stride_size)
#     windows = np.lib.stride_tricks.as_strided(samples, shape = nshape, strides = nstrides)
#     assert np.all(windows[:, 1] == samples[stride_size:(stride_size + window_size)])
#
#     # window wieghting, sFFT, scaling
#     weighting = np.hanning(window_size)[:, None]
#
#     fft = np.fft.rfft(windows * weighting, axis=0)
#     fft = np.absolute(fft)
#     fft = fft**2
#     scale = np.sum(weighting**2) * sample_rate
#     fft[1:-1, :] *= (2.0 / scale)
#     fft[(0, -1), :] /= scale
#
#     # prepare fft frequency list
#     freqs = float(sample_rate) /window_size * np.arange(fft.shape[0])
#
#     # compute spectrogram feature
#
#     ind = np.where(freqs <= max_freq)[0][-1] + 1
#     specgram = np.log(fft[:window_size, :] + eps)
#     return specgram
#
# specgram_map = spectrogram(samples, sampling_rate, max_freq=12000)
#
# fig, ax = plt.subplots()
# im = ax.imshow(specgram_map)

