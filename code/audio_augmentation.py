from pedalboard import Pedalboard, Plugin, Compressor, Chorus, Delay, Gain, Phaser, Reverb, PitchShift, HighpassFilter, LowpassFilter, Distortion
import numpy as np
import random
import librosa

pedal_dict = {
    "compressor": {
        "pedal": Compressor,
        "param_dict": {
            "threshold_db": (-30.0, -10.0),
            "ratio": (1.5, 3.0)
        }
    },
    "chorus": {
        "pedal": Chorus,
        "param_dict": {
            "rate_hz": (0.5, 0.8),
            "depth": (0.05, 0.15)
        }
    },
    
    "reverb": {
        "pedal": Reverb,
        "param_dict": {
            "room_size": (0.1, 0.5),
            "damping": (0.3, 0.9),
            "wet_level": (0.3, 0.7),
            "dry_level": (0.3, 0.7)
        }
    },
    
    "distortion": {
        "pedal": Distortion,
        "param_dict": {
            "drive_db": [1,3]
        }
    },
    
    "lowpassfilter": {
        "pedal": LowpassFilter,
        "param_dict": {
            "cutoff_frequency_hz": (4000,6000)
        }
    },
    
    "highpassfilter": {
        "pedal": HighpassFilter,
        "param_dict": {
            "cutoff_frequency_hz": (100, 500)
        }
    },
    
    "pitchshift": {
        "pedal": PitchShift,
        "param_dict": {
            "semitones": ([-2,-1,1,2],None)
        }
    }
}

def roll_pedal(pedal: Plugin, param_dict: dict[str: tuple], pedal_prob: float=1.0, random_seed: int=None):
    
    if random_seed:
        random.seed(random_seed)
    
    if random.random() > pedal_prob:
        return None
    
    else:   
        roll_dict = {}
        for param, (start, stop) in param_dict.items():
            
            if type(start) == float:
                roll = random.uniform(start, stop)
            elif type(start) == int:
                roll = random.randint(start, stop)
            elif type(start) == list:
                roll = random.choice(start)

            roll_dict[param] = roll

        return pedal(**roll_dict)
    

def process_track(audio: np.ndarray, sample_rate: float, pedals: list[Plugin], fallback: list[Plugin] = None):
    
    n_pedals = sum([1 for pedal in pedals if pedal is not None])
    
    if fallback is None:
        assert n_pedals  >= 1, """No valid pedals were passed and no fallback plugins specified.
            Please provide either a fallback plugin list or implement appropriate exception handling your code."""
    else:
        if n_pedals >= 1:
            board = Pedalboard([pedal for pedal in pedals if pedal])
        else:
            board = Pedalboard([pedal for pedal in fallback])
    
    audio_processed = board(audio, sample_rate)
    audio_processed = librosa.util.normalize(audio_processed)
    
    return audio_processed
