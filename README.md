<br />
<div align="center">
  <h3 align="center">Pedalboard Audio Augmentation</h3>

  <p align="center">
    Utility for using Spotify's Pedalboard library for natural audio data augmentation!
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This library used Spotify's Pedalboard library to enable natural audio data augmentation according to best practices. It comes with
* an audio augmentation module that implements random, natural effect chains for audio augmentation.
* example scripts for applying these random, natural augmentations to individual files or as part of a feature extraction pipeline.
* some example audio files from the GTZAN dataset which you can use to play around with audio augmentations.

Currently, this project implements 7 effect pedals:
1. Compressor (```"compressor"```)
2. Chorus (```"chorus"```)
3. Reverb (```"reverb"```)
4. Distortion (```"distortion"```)
5. Low-Pass Filter (```"lowpass"```)
6. High-Pass Filter (```"highpass"```)
7. Pitch Shift (```"pitchshift"```)

For each of these effects, a natural parameter range is stored as a prebuilt template. Using this or your own template, you can roll random configurations of the pedal for more diverse audio augmentations.

### Built With

The major libraries/tools used in this project are:

* Pedalboard
* Librosa
* Numpy
* Soundfile
* FFmpeg

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these steps.

### Prerequisites

Please make sure FFmpeg is installed on your system. If that is not the case, following [these instructions](https://www.hostinger.com/tutorials/how-to-install-ffmpeg) to install it.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MaxHilsdorf/pedalboard_audio_augmentation
   ```
2. Navigate into the repository in your terminal
    ```sh
    cd path/to/repository
    ```
3. (optional) Setup a new conda environment
    ```sh
    conda create --name pedalboard_aug
    ```
4. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage

### Main functionalities
The main functionalities of this project are included in ```code/audio_augmentation.py```. There, you will find:
* ```pedal_dict``` (dict):

Holds parameter ranges for all the implemented pedals. Adjust to your liking!
* ```roll_pedal(```pedal: Plugin, param_dict: dict[str: tuple], pedal_prob: float=1.0, random_seed: int=None```)``` -> Plugin

Instantiates a given pedalboard pedal using random parameters in pre-defined ranges.
* ```process_track(```audio: np.ndarray, sample_rate: float, pedals: list[Plugin], fallback: list[Plugin] = None```)``` -> np.ndarray

Applies a list of pedalboard effects to an input audio signal.

### Examples
There are some practical example scripts and notebooks in ```examples/``` that cover different use cases:
1. ```pedalboard_basic_usage.ipynb```: Basics of using the pedalboard library.
2. ```augment_single_example.ipynb```: Using random augmentation on a single example.
3. ```augment_examples.py```: Using random augmentation to augment and export multiple files.
4. ```create_augmented_dataset.py```: Example of efficient integration of audio augmentation in feature extraction pipeline.


<!-- ROADMAP -->
## Roadmap
No roadmap defined.

## Issues
No issues recorded.


<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License.



<!-- CONTACT -->
## Contact

Max Hilsdorf - [Medium](https://medium.com/@maxhilsdorf) - [LinkedIn](https://www.linkedin.com/in/max-hilsdorf/) - m.hilsdorf1@gmail.com