import random
import os

import numpy as np

from deep_speaker.audio import read_mfcc, mfcc_fbank
from deep_speaker.batcher import sample_from_mfcc
from deep_speaker.constants import SAMPLE_RATE, NUM_FRAMES
from deep_speaker.conv_models import DeepSpeakerModel
from deep_speaker.test import batch_cosine_similarity

np.random.seed(123)
random.seed(123)

model = DeepSpeakerModel()

model.m.load_weights('./files/models/deep_speaker.h5', by_name=True)

# Code taken Phillpperemy, developer of Deep-Speaker and slightly modified to work with bytes
def read_mfcc_bytes(audio_array, sample_rate):
    return mfcc_fbank(clean_audio(audio_array), sample_rate)

def clean_audio(audio):
    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]
    return audio[offsets[0]:offsets[-1]]

# Original Sample Code from: Phillpperemy, developer of Deep-Speaker https://github.com/philipperemy/deep-speaker
def calculate_similarity_files(filepath_1, filepath_2):

    mfcc_001 = sample_from_mfcc(read_mfcc(filepath_1, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc(filepath_2, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)

def calculate_similarity(sample_file, audio_array):

    mfcc_001 = sample_from_mfcc(read_mfcc(sample_file, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc_bytes(audio_array, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)
