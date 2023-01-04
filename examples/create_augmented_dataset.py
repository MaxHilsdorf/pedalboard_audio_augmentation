from pedalboard import Compressor, PitchShift, HighpassFilter
import sys
import numpy as np
import pandas as pd
import librosa
import os
from tqdm import tqdm

sys.path.append("../code/")
from audio_augmentation import roll_pedal, pedal_dict, process_track


## UTILITY FUNCTIONS ##

def get_n_frames(n_samples, window_length, hop_length):
    return int(n_samples/hop_length - window_length/hop_length + 3)


## BASIC PARAMETERS ##

N_MELS = 120
HOP_LENGTH = 512 # = overlap
N_FFT = 1024 # = window length
TARGET_SR = 22050
SNIPPET_LENGTH = 30
TARGET_N_SAMPLES = TARGET_SR*SNIPPET_LENGTH


## PEDAL SETTINGS ##

pedal_config = [("compressor", .3),
                ("chorus", .3),
                ("reverb", .3),
                ("distortion", .3),
                ("lowpassfilter", .3),
                ("highpassfilter", .3),
                ("pitchshift", .3)
                ]

fallback = [HighpassFilter(cutoff_frequency_hz=300),
            PitchShift(semitones=1),
            Compressor(threshold_db=-10, ratio=1.3)]


## LOAD DATASET ##

df_train = pd.read_csv("../audio_data/gtzan_mini/gtzan_mini_train.csv")
df_test = pd.read_csv("../audio_data/gtzan_mini/gtzan_mini_test.csv")


## PREPARE ARRAYS FOR FEATURES AND LABELS ##

n_rows = int(len(df_train)*2 + len(df_test))
n_frames = get_n_frames(TARGET_N_SAMPLES, N_FFT, HOP_LENGTH)
specs = np.zeros((n_rows, N_MELS, n_frames))
labels = []


## FILL ARRAYS ##

for i, row in tqdm(df_train.iterrows(), total=len(df_train)):

    # Store label
    labels.append(row["label"])
    
    # Read and pad/truncate audio
    audio, is_sr = librosa.load(row["path"])
    if is_sr != TARGET_SR:
        audio = librosa.resample(audio, is_sr, TARGET_SR)
    
    if len(audio) > TARGET_N_SAMPLES:
        audio = audio[:TARGET_N_SAMPLES]
    
    elif len(audio) < TARGET_N_SAMPLES:
        audio = np.pad(audio, ((0, TARGET_N_SAMPLES - len(audio))))
    
    # Roll pedals
    pedal_rolls = [roll_pedal(pedal=pedal_dict[pedal]["pedal"],
                          param_dict=pedal_dict[pedal]["param_dict"],
                          pedal_prob=prob,
                          random_seed=42+i)
               for pedal, prob in pedal_config]
    
    # Apply pedalboard
    audio_aug = process_track(audio, sample_rate=TARGET_SR, pedals=pedal_rolls, fallback=fallback)
    
    # Get melspecs
    spec = librosa.feature.melspectrogram(y=audio, sr=TARGET_SR, n_fft=N_FFT, n_mels=N_MELS)
    spec_aug = librosa.feature.melspectrogram(y=audio_aug, sr=TARGET_SR, n_fft=N_FFT, n_mels=N_MELS)
    specs[i,...] = spec


## EXPORT ARRAYS ##
np.save("../audio_data/gtzan_mini/spectrogram_dataset_aug.npy", specs)
