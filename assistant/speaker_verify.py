import random
import os
from config.config_variables import max_users

from mutagen.wave import WAVE
import numpy as np

from scipy.io.wavfile import write

from deep_speaker.audio import read_mfcc, mfcc_fbank
from deep_speaker.batcher import sample_from_mfcc
from deep_speaker.constants import SAMPLE_RATE, NUM_FRAMES
from deep_speaker.conv_models import DeepSpeakerModel
from deep_speaker.test import batch_cosine_similarity

np.random.seed(123)
random.seed(123)

model2 = DeepSpeakerModel()

model2.m.load_weights('../ResCNN_triplet_training_checkpoint_265.h5', by_name=True)


def audio_file_length(audio_file):
    audio = WAVE(audio_file) 
    audio_info = audio.info 
    length = int(audio_info.length) 
    return length

# Code taken Phillpperemy, developer of Deep-Speaker and slightly modified to work with bytes
def read_mfcc_bytes(audio_array, sample_rate):
    audio = audio_array # line modified
    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]
    # left_blank_duration_ms = (1000.0 * offsets[0]) // self.sample_rate  # frame_id to duration (ms)
    # right_blank_duration_ms = (1000.0 * (len(audio) - offsets[-1])) // self.sample_rate
    # TODO: could use trim_silence() here or a better VAD.
    audio_voice_only = audio[offsets[0]:offsets[-1]]
    mfcc = mfcc_fbank(audio_voice_only, sample_rate)
    return mfcc



# Original Sample Code from: Phillpperemy, developer of Deep-Speaker https://github.com/philipperemy/deep-speaker
def speaker_verify(filepath_1, filepath_2):

    mfcc_001 = sample_from_mfcc(read_mfcc(filepath_1, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc(filepath_2, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model2.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model2.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)

def speaker_verify_2(sample_file, audio_array):

    mfcc_001 = sample_from_mfcc(read_mfcc(sample_file, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc_bytes(audio_array, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model2.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model2.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)
