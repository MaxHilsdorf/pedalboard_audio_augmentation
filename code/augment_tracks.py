from pedalboard import Pedalboard, Plugin, Compressor, Chorus, Delay, Gain, Phaser, Reverb, PitchShift, HighpassFilter, LowpassFilter, Distortion
import audio_augmentation
from audio_augmentation import roll_pedal, pedal_dict, process_track
import numpy as np
import librosa
import soundfile as sf
import os


FILE_PATHS = [
    "../audio_data/dev_tracks/" + name for name in os.listdir("../audio_data/dev_tracks/")
]

OUT_DIR = "../audio_data/dev_tracks_aug/"
if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)


## ROLL PEDALS ##

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

pedal_rolls = [roll_pedal(pedal=pedal_dict[pedal]["pedal"],
                          param_dict=pedal_dict[pedal]["param_dict"],
                          pedal_prob=prob,
                          random_seed=None)
               for pedal, prob in pedal_config]

print("Pedal Rolls:")
for pedal in pedal_rolls:
    print(pedal)


## APPLY BOARD ##

for fp in FILE_PATHS:
    
    track_dir = "/".join(fp.split("/")[:-1]) + "/"
    track_name = fp.split("/")[-1]
    
    track_prefix = ".".join(track_name.split(".")[:-1])
    track_suffix = track_name.split(".")[-1]
    
    audio, sr = librosa.load(track_dir + track_name)
    audio_processed = process_track(audio, sample_rate=sr, pedals=pedal_rolls, fallback=fallback)

    sf.write(file=f"{OUT_DIR}{track_prefix}_processed.wav", data=audio_processed, samplerate=sr)
