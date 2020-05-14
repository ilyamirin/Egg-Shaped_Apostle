import librosa
from matplotlib import pyplot as plt
import numpy as np
import scipy
from librosa import display
import datetime

# get filenames
file_1, file_2 = '2_2_0_2020-03-24T17_35_33.087154.wav', '2_1_0_2020-03-24T17_35_33.077595.wav'

# set format of date in filename
format = '%Y-%m-%dT%H_%M_%S.%f'


# format date to datetime.timestamp
def get_timestamp(filename):
    timestamp = filename[6:-4]
    return datetime.datetime.strptime(timestamp, format)


# sort files by start time and get their delay in secs
def sort_start_time(file_1, file_2):
    ts_1 = get_timestamp(file_1)
    ts_2 = get_timestamp(file_2)
    if ts_1 > ts_2:
        return file_2, file_1, (ts_1 - ts_2).microseconds*1e-6
    else:
        return file_1, file_2, (ts_2 - ts_1).microseconds*1e-6


# redefine files by sorting result
file_1, file_2, delay = sort_start_time(file_1, file_2)
# get samples and sampling rate (sr) from files
samples1, sr = librosa.load(file_1)
samples2, *_ = librosa.load(file_2)
# cut off start of first samples array by delay
samples1 = samples1[int(sr*delay):]


def get_sync_delay(samples1, samples2, sr):
    eps_t = 1
    slice_size = int(sr * eps_t)
    slice1 = samples1[:slice_size]
    slice2 = samples2[:slice_size]

    # сравнение двух аудио по абсолютной разнице
    mse_list = []
    for i in range(slice_size)[1:slice_size//2]:
        slice1_temp = slice1[i:]
        slice2_temp = slice2[:-i]
        mse_list.append(np.mean((np.abs(slice1_temp) - np.abs(slice2_temp))**2))
    return np.argmin(mse_list)


# cut off start of first samples array by computed delay where MSE between two signals is minimal
samples1 = samples1[get_sync_delay(samples1, samples2, sr):]
samples2 = samples2[:len(samples1)]
# librosa.output.write_wav('synchronized untitled1.wav', samples1, sampling_rate1)


def fft_plot(audio, sampling_rate, name):
    plt.figure()
    n = len(audio)
    T = 1/sampling_rate
    yf = scipy.fft.fft(audio)
    xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.grid()
    plt.xlabel('freq ->')
    plt.ylabel('magnitude')
    plt.savefig(name+'_fft.png')
    return yf


batch_size = 512
# batch_size = sr
samples_len = len(samples1)
batch_count = samples_len // batch_size\
    if samples_len % batch_size == 0\
    else (samples_len // batch_size) + 1

denoised_list_ifft = np.array([])

for i in range(batch_count):
    start = i*batch_size
    end = (i+1)*batch_size
    fft_list1 = scipy.fft.fft(samples1[start:end])
    fft_list2 = scipy.fft.fft(samples2[start:end])
    fft_list_result = np.array([], dtype=np.complex)
    # for j in range(len(fft_list1)):
        # print(fft_list1[i]-fft_list2[i])
        # threshold = abs(2.55+2.55j)
        # if abs(fft_list1[j]-fft_list2[j]) < threshold:
        #     print(1)

        # diff = fft_list1[j] - fft_list2[j]
        # fft_list_result = np.append(fft_list_result, diff)
        # else:
        #     print(2)
        #     fft_list_result.append((fft_list1[j]-fft_list2[j])/10)

    # cutoff by freqs
    fft_list_result = fft_list1-fft_list2
    n = len(fft_list_result)
    T = 1/sr
    freqs = np.linspace(0.0, 1.0 / (2.0 * T), n//2)
    if n % 2 != 0:
        freqs = np.append(freqs, freqs[-1]+1.0/(2.0 * T))
        freqs = np.append(freqs, np.flip(freqs)[:-1])
    else:
        freqs = np.append(freqs, np.flip(freqs))
    min = 150
    max = 8000
    fft_list_result[freqs < min] = 0.0+0.0j
    fft_list_result[freqs > max] = 0.0+0.0j
    denoised_list_ifft = np.append(denoised_list_ifft, scipy.fft.ifft(fft_list_result))

a = np.array([i.real for i in denoised_list_ifft])
librosa.output.write_wav('ifft.wav', a, sr)
#librosa.output.write_wav('denoised.wav', samples1-a, sr)
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

