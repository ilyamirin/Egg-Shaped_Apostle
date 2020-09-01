#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# std libs imports
import os
from datetime import datetime

# ext libs imports
import numpy as np
import librosa

DATA_DIR = os.path.join(os.getcwd(), 'data')


# format date to datetime.timestamp
def get_timestamp(filename):
    timestamp = filename[6:-4]
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')


# sort files by start time and get their delay in secs,
# return files in asc order of start time, delay and (are files switched?)
def sort_start_time(file_1, file_2):
    ts_1 = get_timestamp(file_1)
    ts_2 = get_timestamp(file_2)
    if ts_1 > ts_2:
        return file_2, file_1, (ts_1 - ts_2).microseconds * 1e-6, False
    else:
        return file_1, file_2, (ts_2 - ts_1).microseconds * 1e-6, True


# return  samples that were synchronized by rec time metadata
def get_syncd_by_time_samples(file_1, file_2):
    file_1, file_2, delay, switch_flag = sort_start_time(file_1, file_2)
    samples1, sr = librosa.load(os.path.join(DATA_DIR, file_1), sr=None)
    delay = int(delay * sr)
    samples1 = np.append(samples1[delay:], np.array([0]*delay))
    samples2, *_ = librosa.load(os.path.join(DATA_DIR, file_2), sr=None)
    return samples1, samples2, sr, switch_flag, delay


# mse between 2 signals, return delay in samples
def get_sync_delay(samples1, samples2, sr, eps_t=1):
    slice_size = int(sr * eps_t)
    slice1 = samples1[:slice_size]
    slice2 = samples2[:slice_size]
    mse_list = []
    for i in range(slice_size)[1:slice_size//2]:
        slice1_temp = slice1[i:]
        slice2_temp = slice2[:-i]
        mse_list.append(np.mean((np.abs(slice1_temp) - np.abs(slice2_temp))**2))
    return np.argmin(mse_list)


# gets filnames and return their sum delay all delays in samples
def synchronize(file_1, file_2):
    samples1, samples2, sr, switch_flag, delay_time = get_syncd_by_time_samples(file_1, file_2)
    delay_signal = get_sync_delay(samples1, samples2, sr)
    syncd_samples1 = np.append(samples1[delay_signal:], np.array([0]*delay_signal))
    return syncd_samples1, samples2, sr, delay_signal


# file_1 = '0_2_0_2020-06-20T17:19:31.093728.wav'
# file_2 = '0_3_0_2020-06-20T17:19:31.093825.wav'
# print(synchronize(file_1, file_2))
