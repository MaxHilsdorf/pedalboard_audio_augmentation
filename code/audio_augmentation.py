from pedalboard import Pedalboard, Plugin, Compressor, Chorus, Delay, Gain, Phaser, Reverb, PitchShift, HighpassFilter, LowpassFilter, Distortion
import numpy as np
import random
import librosa


## PREBUILT CONFIGURATION ##

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
            "drive_db": (1,3)
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


## FUNCTIONS ##

def roll_pedal(pedal: Plugin, param_dict: dict[str: tuple], pedal_prob: float=1.0, random_seed: int=None) -> Plugin:
    """Instantiates a given pedalboard pedal using random parameters in pre-defined ranges.
    
    Args:
        pedal (Plugin): The pedal to use (e.g. Compressor)
        param_dict (dict): {"param1": (param_range), "param2": (param_range), ...}
            <param_range> can be implemented in three ways:
                1. Continuous range -> param_range = (start, end), where <start>, <end> are floats.
                2. Discrete range -> param_range = (start, end), where <start>, <end> are integers.
                3. Set -> param_range = ([element_1, element_2, ...], None), where <element_x> can be any type.
        pedal_prob (float, optional): Probability that a roll "succeeds".
            If the roll does not "succeed", None is returned instead of a pedal instance.
            Defaults to 1.0.
        random_seed (int, optional): Random Seed for roll (int) or None. Defaults to None.

    Returns:
        Plugin: An instance of the given pedal with randomly selected parameters.
    """
    
    if random_seed:
        random.seed(random_seed)
    
    # Decide is the roll is "succesfull" at all
    if random.random() > pedal_prob:
        return None
    
    # If roll "succeeds", select random parameters
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
    

def process_track(audio: np.ndarray, sample_rate: float, pedals: list[Plugin], fallback: list[Plugin] = None) -> np.ndarray:
    """Applies a list of pedalboard effects to an input audio signal.

    Args:
        audio (np.ndarray): Input audio as waveform array.
        sample_rate (float): Sample rate of the signal.
        pedals (list[Plugin or None]): Pedal instances or None.
        fallback (list[Plugin], optional): Pedals to use if <pedal> consist only of None values. Defaults to None.

    Returns:
        np.ndarray: Processed audio
    """    
    
    # Check if there is at least one pedal in the given pedal list
    # If not, raise error if no fallback is implemented
    n_pedals = sum([1 for pedal in pedals if pedal is not None])
    
    if fallback is None:
        assert n_pedals  >= 1, """No valid pedals were passed and no fallback plugins specified.
            Please provide either a fallback plugin list or implement appropriate exception handling your code."""
    
    # Aggregate either rolled pedals or fallback pedals to pedalboard
    else:
        if n_pedals >= 1:
            board = Pedalboard([pedal for pedal in pedals if pedal])
        else:
            board = Pedalboard([pedal for pedal in fallback])
    
    # Apply pedalboard
    audio_processed = board(audio, sample_rate)
    audio_processed = librosa.util.normalize(audio_processed)
    
    return audio_processed
